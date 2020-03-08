import os
from pydiogment import auga, augf, augt


def augment_file(test_file):
    """
    Generate audio augmentations from one file.
    """
    try:
        augt.slowdown(test_file, coefficient=0.8)
    except Exception:
        print("cannot %10s for %20s" % ("slowdown", test_file))

    try:
        augt.speed(test_file, coefficient=1.2)
    except Exception:
        print("cannot %10s for %20s" % ("speed", test_file))

    try:
        augt.random_cropping(test_file, 1)
    except Exception:
        print("cannot %10s for %20s" % ("random_cropping", test_file))

    try:
        augt.shift_time(test_file, 1, "right")
    except Exception:
        print("cannot %10s for %20s" % ("shift_time", test_file))

    try:
        augt.shift_time(test_file, 1, "left")
    except Exception:
        print("cannot %10s for %20s" % ("shift_time", test_file))

    try:
        auga.add_noise(test_file, 10)
    except Exception:
        print("cannot %10s for %20s" % ("add_noise", test_file))

    try:
        auga.fade_in_and_out(test_file)
    except:
        print("cannot %10s for %20s" % ("fade_in_and_out", test_file))

    try:
        auga.apply_gain(test_file, -100)
    except Exception:
        print("cannot %10s for %20s" % ("apply_gain", test_file))

    try:
        auga.apply_gain(test_file, -50)
    except Exception:
        print("cannot %10s for %20s" % ("apply_gain", test_file))

    try:
        augf.convolve(test_file, "noise", 10**-2.75)
    except Exception:
        print("cannot %10s for %20s" % ("convolve", test_file))

    try:
        augf.change_tone(test_file, .9)
    except Exception:
        print("cannot %10s for %20s" % ("change_tone", test_file))

    try:
        augf.change_tone(test_file, 1.1)
    except Exception:
        print("cannot %10s for %20s" % ("change_tone", test_file))


if __name__ == "__main__":
    folder = "data/waves/"

    # collect paths to wave files
    wave_fnames = [os.path.join(root, file)
                   for root, dirs, files in os.walk(folder)
                   for file in files]

    # print
    print("-" * 61)
    print("                      Start Augmenting                       ")
    print("-" * 61)

    # augment files
    for wave_fname in wave_fnames[:]:
        augment_file(wave_fname)
        print("-" * 61)
