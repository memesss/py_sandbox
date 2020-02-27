import numpy


compressed_stream = [66, 22, 70, 26, 66, 19, 69, 19, 79, 18, 70, 18, 66, 20, 73, 21, 72, 18, 68, 18, 73, 20, 79, 21, 19, 68, 18, 79, 29, 72, 35, 65, 23, 65, 30, 70, 21, 66, 31, 20, 76, 28, 73, 22, 71, 19, 76, 23, 72, 20, 65, 20, 72, 18, 72, 18, 81, 34, 65, 31, 25, 68, 29, 77, 34, 71, 19, 85, 32, 69, 19, 71, 30, 74, 32, 66, 19, 65, 18, 66, 27, 67, 20, 82, 25, 85, 58, 71, 22, 78, 22, 65, 31, 67, 20, 72, 27, 72, 52, 68, 28, 65, 18, 66, 32, 67, 19, 67, 22, 72, 34, 72, 21, 71, 18, 83, 36, 52, 76, 21, 75, 25, 67, 19, 65, 21, 87, 19, 66, 25, 70, 23, 66, 29, 79, 29, 66, 22, 75, 19, 67, 36, 36, 72, 18, 72, 18, 68, 19, 70, 29, 67, 22, 72, 21, 70, 28, 66, 38, 77, 25, 96, 19, 68, 22, 71, 36, 69, 58, 69, 29, 68, 21, 67, 20, 28, 66, 41, 73, 19, 22, 72, 32, 68, 48, 78, 23, 69, 20, 65, 21, 85, 29, 85, 26, 77, 31, 69, 23, 74, 37, 23, 67, 32, 76, 45, 66, 23, 26, 83, 28, 69, 27, 69, 23, 65, 18, 74, 32, 69, 22, 68, 19, 66, 18, 66, 26, 69, 37, 83, 20, 67, 21, 65, 26, 68, 23, 80, 33, 19, 78, 20, 69, 22, 70, 33, 69, 19, 88, 23, 67, 128, 79, 68, 33, 70, 30, 38, 76, 25, 113, 20, 74, 45, 73, 24, 72, 43, 69, 25, 68, 26, 67, 22, 18, 67, 29, 68, 18, 70, 26, 68, 128, 70, 77, 22, 69, 18, 70, 20, 68, 30, 31, 69, 22, 67, 21, 70, 40, 78, 18, 68, 32, 70, 29, 70, 27, 73, 27, 100, 20, 73, 18, 72, 23, 68, 18, 73, 26, 102, 55, 62, 69, 18, 72, 20, 73, 19, 68, 34, 73, 27, 69, 36, 65, 23, 65, 47, 78, 24, 41, 79, 21, 71, 28, 71, 25, 73, 27, 72, 18, 78, 29, 68, 25, 128, 85, 128, 85, 69, 128, 112, 110, 18, 77, 25, 69, 23, 67, 20, 88, 30, 72, 22, 80, 18, 19, 24, 69, 128, 92, 128, 97, 73, 19, 83, 26, 73, 18, 91, 26, 77, 22, 34, 66, 33, 18, 192, 70, 29, 79, 19, 88, 24, 78, 21, 72, 47, 68, 27, 95, 18, 71, 32, 65, 49, 69, 32, 76, 36, 67, 31, 68, 21, 68, 33, 68, 21, 72, 128, 66, 66, 22, 72, 24, 72, 19, 20, 80, 25, 67, 26, 77, 29, 28, 77, 21, 67, 34, 66, 23, 39, 18, 76, 26, 67, 18, 22, 71, 60, 73, 29, 95, 36, 77, 19, 78, 19, 21, 31, 69, 20, 73, 26, 29, 71, 18, 82, 34, 76, 22, 77, 18, 71, 32, 77, 28, 67, 18, 192, 71, 26, 69, 18, 76, 36, 74, 18, 67]

zeros_mask = 0x40
continue_mask = 0x80

def check_if_zeros (byte):
    if (byte & zeros_mask) == 0:
        return False
    else:
        return True

def check_if_continue (byte):
    if (byte & continue_mask) == 0:
        return False
    else:
        return True
        
def get_val_from_single_byte(byte):
    return (~zeros_mask & byte)
    
def get_val_from_hbyte(byte):
    return (~zeros_mask & byte & ~continue_mask)

def item(i):
    return compressed_stream[i] 
    
print ("commpressed_stream.len()->", len(compressed_stream))


mono_uncomp_roi = []

i=0;
while i < len(compressed_stream):
    #zeros
    if check_if_zeros(item(i)) and not check_if_continue(item(i)):
        for z in range (0, get_val_from_single_byte(item(i))):
            mono_uncomp_roi.append (0)
        i = i + 1
        
    else:
        if check_if_zeros(item(i)) and check_if_continue(item(i)):
          lbyte = compressed_stream[i + 1]
          hbyte = get_val_from_hbyte(item(i))
          zeros = hbyte * 256 + lbyte
          for z in range (0, zeros):
            mono_uncomp_roi.append (0)
          i = i + 2
        else:
    #ADCs    
            if not check_if_zeros(item(i)) and not check_if_continue(item(i)):
                mono_uncomp_roi.append (get_val_from_single_byte(item(i)))
                i = i + 1
        
            else:
                if not check_if_zeros(item(i)) and check_if_continue(item(i)):
                    lbyte = compressed_stream[i + 1]
                    hbyte = get_val_from_hbyte(item(i))
                    adcs = hbyte * 256 + lbyte
                    mono_uncomp_roi.append (adcs)
                    i = i + 2
        
print (mono_uncomp_roi)
print (len(mono_uncomp_roi))
histo = numpy.histogram(mono_uncomp_roi)
print (histo)
        
    