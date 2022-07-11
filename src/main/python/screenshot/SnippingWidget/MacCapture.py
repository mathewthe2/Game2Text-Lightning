import Quartz
from Cocoa import NSURL
import Quartz.CoreGraphics as CG
from AppKit import NSScreen
# import LaunchServices

def cartesian_capture(x, y, width, height, total_width, total_height, path):
    screen_width = NSScreen.mainScreen().frame().size.width
    screen_height = NSScreen.mainScreen().frame().size.height
    x += (screen_width - total_width)
    y += 2 * (screen_height - total_height) # not sure why it needs to be x2
    region = CG.CGRectMake(x, y, width, height)
    screenshot(path, region=region)

def screenshot(path, region = None):
    """region should be a CGRect, something like:

    >>> import Quartz.CoreGraphics as CG
    >>> region = CG.CGRectMake(0, 0, 100, 100)
    >>> sp = ScreenPixel()
    >>> sp.capture(region=region)

    The default region is CG.CGRectInfinite (captures the full screen)
    """

    if region is None:
        region = CG.CGRectInfinite

    # Create screenshot as CGImage
    image = CG.CGWindowListCreateImage(
        region,
        CG.kCGWindowListOptionOnScreenOnly,
        CG.kCGNullWindowID,
        CG.kCGWindowImageDefault)

    dpi = 72 # FIXME: Should query this from somewhere, e.g for retina displays

    url = NSURL.fileURLWithPath_(path)

    dest = Quartz.CGImageDestinationCreateWithURL(
        url,
        'public.png', # LaunchServices.kUTTypePNG
        1, # 1 image in file
        None
        )

    properties = {
        Quartz.kCGImagePropertyDPIWidth: dpi,
        Quartz.kCGImagePropertyDPIHeight: dpi,
        }

    # Add the image to the destination, characterizing the image with
    # the properties dictionary.
    Quartz.CGImageDestinationAddImage(dest, image, properties)

    # When all the images (only 1 in this example) are added to the destination, 
    # finalize the CGImageDestination object. 
    Quartz.CGImageDestinationFinalize(dest)


if __name__ == '__main__':
    print(NSScreen.mainScreen().frame())
    print(NSScreen.mainScreen().frame().size.width)
    print(NSScreen.mainScreen().frame().size.height)
    # Capture full screen
    # screenshot("testscreenshot_full.png")

    # Capture region (100x100 box from top-left)
    # region = CG.CGRectMake(0, 0, 100, 100)
    # screenshot("testscreenshot_partial.png", region=region)