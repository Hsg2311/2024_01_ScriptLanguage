import PIL.Image
import PIL.ImageTk
import PIL.ImageSequence

class GIFAnimation:
    def __init__(self, w, h):  
        src = PIL.Image.open('res/richard.gif')

        frames = []
        disposal = []
        for gifFrame in PIL.ImageSequence.Iterator(src):
            disposal.append(gifFrame.disposal_method)
            frames.append(gifFrame.convert('P'))

        # Loop through frames, and edit them based on their disposal method
        self.__frames = []
        lastFrame = None
        thisFrame = None
        for i, loadedFrame in enumerate(frames):
            # Update thisFrame
            thisFrame = loadedFrame

            # If the disposal method is 2
            if disposal[i] == 2:
                # Check that this is not the first frame
                if i != 0:
                    # Pastes thisFrames opaque pixels over lastFrame and appends lastFrame to output
                    lastFrame.paste(thisFrame, mask=thisFrame.convert('RGBA'))
                    self.__frames.append(lastFrame)
                else:
                    self.__frames.append(thisFrame)

            # If the disposal method is 1 or 0
            elif disposal[i] == 1 or disposal[i] == 0:
                # Appends thisFrame to output
                self.__frames.append(thisFrame)

            # If disposal method if anything other than 2, 1, or 0
            else:
                raise ValueError('Disposal Methods other than 2:Restore to Background, 1:Do Not Dispose, and 0:No Disposal are supported at this time')

            # Update lastFrame
            lastFrame = loadedFrame

        self.__index = 0
        self.__frames = [frame.resize((w, h)) for frame in self.__frames]
        self.__frames = [PIL.ImageTk.PhotoImage(frame) for frame in self.__frames]

    def advance(self):
        self.__index = (self.__index + 1) % len(self.__frames)

    def image(self):
        return self.__frames[self.__index]