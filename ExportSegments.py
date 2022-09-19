#PY  <- Needed to identify #
# Script for exporting segments using copy codec if possible
# Martin Holý 2022

# 2022.09.15
# - bug fix: using copy codec for segment which starts on key frame and ends on end of the video
# - bug fix: time in round bug (seconds or minutes > 59)
# - add: decode time taken from file name (YYMMDD_HHmmss) and append time in of segment to it

def lstrip(s, x):
  found = True
  out = ""

  for c in s:
    if found:
      if c == x:
        continue
      else:
        found = False
    out += c
  
  return out

def substring(string, start, stop):
  len = stop - start
  out = ""
  i = 0

  for c in string[start:]:
    if i == len : break
    out += c
    i += 1

  return out

adm = Avidemux()
ed = Editor()

def isKeyframe(pts):
  return pts == ed.getPrevKFramePts(pts+1)

def getSegments():
  segments = []
  for idx in range(ed.nbSegments()):
    segments.append([
      ed.getTimeOffsetForSegment(idx),
      ed.getDurationForSegment(idx)])
  return segments

def addSegments(segments):
  for segment in segments:
    adm.addSegment(0, segment[0], segment[1])

def resetEdit():
  adm.clearSegments()
  adm.addSegment(0, 0, ed.getRefVideoDuration(0))

def getOffset():
  return ed.getPts(0)

def getFileName():
  return splitext(ed.getRefVideoName(0))[0].split("/")[-1]

def ptsToStr(pts, sep, hours=True, intSec=True):
  s = pts / 1000000
  h = int(s / 3600)
  s -= h * 3600
  m = int(s / 60)
  s -= m * 60

  if intSec:
    s = round(s)
    if s == 60:
      m += 1
      s = 0
      if m == 60:
        h += 1
        m = 0
    ss = str(int(s))
  else:
    # little tinypy limitations walk around
    a = int(s)
    b = int((s - a) * 100)
    s = round(s * 100) / 100
    ss = str(a) + "." + str(b)

  sh = str(h)
  sm = str(m)
  if (h < 10): sh = "0" + sh
  if (m < 10): sm = "0" + sm
  if (s < 10): ss = "0" + ss

  if hours:
    return sh + sep + sm + sep + ss
  else:
    return sm + sep + ss

def timeTakenToPts(timeTaken):
  h = int(lstrip(substring(timeTaken, 0, 2), "0"))
  m = int(lstrip(substring(timeTaken, 2, 4), "0"))
  s = int(lstrip(substring(timeTaken, 4, 6), "0"))
  return (h * 3600 + m * 60 + s) * 1000000

def appendFileName(segments, offset, fileName, sep, timeTakenPts=0):
  hours = timeTakenPts > 0 or (segments[-1][0] - offset) / 1000000.0 / 3600 >= 1
  dict1 = {}

  for segment in segments:
    timeIn = ptsToStr(segment[0] - offset + timeTakenPts, sep, hours, True)
    segment.append(fileName + "_" + timeIn)

    if timeIn in dict1:
      dict1[timeIn].append(segment)
    else:
      dict1[timeIn] = [segment]

  for k in dict1:
    if len(dict1[k]) > 1:
      for segment in dict1[k]:
        segment[2] = fileName + "_" + ptsToStr(segment[0] - offset + timeTakenPts, sep, hours, False)

def exportSegments(segments, offset, outDir):
  vidDur = ed.getRefVideoDuration(0)

  for segment in segments:
    adm.markerA = segment[0] - offset
    adm.markerB = adm.markerA + segment[1]

    if isKeyframe(adm.markerA) and isKeyframe(adm.markerB) or adm.markerB == vidDur:
      adm.audioCodec(0, "copy")
      adm.videoCodec("copy")
      adm.markerB = adm.markerB - 1
    else:
      adm.audioCodec(0, "LavAAC", "bitrate=128")
      adm.videoCodecSetProfile("x264", "x264VerySlow25")

    outFilePath = outDir + segment[2] + ".mp4"
    adm.save(outFilePath)

def main():
  offset = getOffset()
  segments = getSegments()

  decodeTimeTaken = DFToggle("Decode time taken from file name")
  decodeTimeTaken.value = False
  dialog = DialogFactory("Export Segments")
  dialog.addControl(decodeTimeTaken)

  if dialog.show() == 1 and decodeTimeTaken.value:
    # decode time taken from file name (YYMMDD_HHmmss) and append time in of segment to it
    fileName = getFileName()
    dateTaken = substring(fileName, 0, 8)
    timeTaken = substring(fileName, 9, 15)

    timeTakenPts = timeTakenToPts(timeTaken)
    print(timeTaken)
    appendFileName(segments, offset, dateTaken, "", timeTakenPts)
  else:
    # append time in of segment behind file name
    appendFileName(segments, offset, getFileName(), "-")

  resetEdit()
  exportSegments(segments, offset, "d:\\avidemux\\")

  #restore original segments
  adm.clearSegments()
  addSegments(segments)

main()


