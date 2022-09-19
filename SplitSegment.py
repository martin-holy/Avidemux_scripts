#PY  <- Needed to identify #
# Script to split video at current time
# Martin Holý 2022

adm = Avidemux()
ed = Editor()

def getRefCurrentPts():
  totalDuration = 0
  pts = ed.getCurrentPts()

  for idx in range(ed.nbSegments()):
    dur = ed.getDurationForSegment(idx)
    
    if totalDuration + dur >= pts:
      return pts + ed.getTimeOffsetForSegment(idx) - totalDuration
    
    totalDuration += dur

def splitSegment():
  pts = getRefCurrentPts()
  segments = []
  
  for idx in range(ed.nbSegments()):
    offset = ed.getTimeOffsetForSegment(idx)
    dur = ed.getDurationForSegment(idx)

    if (offset <= pts and offset + dur >= pts):
      newDurA = pts - offset
      newDurB = dur - newDurA
      segments.append([offset, newDurA])
      segments.append([pts, newDurB])
    else:
      segments.append([offset, dur])

  adm.clearSegments()
  for segment in segments:
    adm.addSegment(0, segment[0], segment[1])

splitSegment()
