import os
import pydiogment as pdg 


def augment_file(test_file):
    try    : pdg.augt.slowdown(test_file, coefficient=0.8)
    except : print("cannot %10s for %20s" % ("slowdown", test_file))
    
    try    : pdg.augt.speed(test_file, coefficient=1.2)
    except : print("cannot %10s for %20s" % ("speed", test_file))
    
    try    : pdg.augt.random_cropping(test_file, 1)
    except : print("cannot %10s for %20s" % ("random_cropping", test_file))
    
    try    : pdg.augt.shift_time(test_file, 1,"right")
    except : print("cannot %10s for %20s" % ("shift_time", test_file))
    
    try    : pdg.augt.shift_time(test_file, 1,"left")
    except : print("cannot %10s for %20s" % ("shift_time", test_file))
    
    try    : pdg.auga.add_noise(test_file, 10)
    except : print("cannot %10s for %20s" % ("add_noise", test_file))
    
    try    : pdg.auga.fade_in_and_out(test_file)
    except : print("cannot %10s for %20s" % ("fade_in_and_out", test_file))
    
    try    : pdg.auga.apply_gain(test_file, -100)
    except : print("cannot %10s for %20s" % ("apply_gain", test_file))
    
    try    : pdg.auga.apply_gain(test_file, -50)
    except : print("cannot %10s for %20s" % ("apply_gain", test_file))
    
    try    : pdg.augf.convolve(test_file, "noise", 10**-2.75)
    except : print("cannot %10s for %20s" % ("convolve", test_file))
    
    try    : pdg.augf.change_tone(test_file, .9)
    except : print("cannot %10s for %20s" % ("change_tone", test_file))
    
    try    : pdg.augf.change_tone(test_file, 1.1)
    except : print("cannot %10s for %20s" % ("change_tone", test_file))    
    
    
if __name__ == "__main__":
    folder = "data/waves/"
    
    # collect paths to wave files
    wave_fnames = [os.path.join(root, file)
                   for root, dirs, files in os.walk(folder)  for file in files]
    
    # augment files
    for wave_fname in wave_fnames[:]: 
        augment_file(wave_fname)



