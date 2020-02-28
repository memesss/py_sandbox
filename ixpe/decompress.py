import numpy


compressed_stream = [82, 21, 120, 18, 129, 33, 111, 27, 65, 18, 65, 49, 70, 49, 88, 23, 71, 18, 85, 28, 84, 36, 76, 23, 66, 20, 73, 30, 84, 19, 80, 39, 70, 27, 70, 42, 72, 18, 77, 39, 57, 39, 34, 26, 70, 27, 69, 41, 83, 19, 35, 128, 111, 128, 113, 40, 34, 67, 29, 76, 18, 47, 77, 21, 48, 128, 131, 128, 134, 128, 114, 128, 106, 36, 67, 18, 20, 71, 19, 77, 28, 70, 128, 129, 128, 189, 128, 247, 128, 185, 128, 176, 128, 77, 65, 28, 92, 20, 128, 87, 128, 247, 128, 236, 129, 29, 129, 20, 128, 171, 128, 70, 83, 34, 75, 43, 128, 100, 128, 197, 129, 63, 129, 38, 128, 216, 128, 113, 35, 65, 33, 86, 35, 69, 42, 65, 128, 238, 128, 252, 128, 150, 128, 98, 128, 81, 69, 20, 92, 128, 82, 128, 112, 128, 94, 128, 79, 37, 71, 31, 88, 24, 58, 54, 51, 28, 69, 29, 75, 128, 64, 70, 23, 71, 27, 65, 35, 65, 51, 36, 77, 44, 84, 26, 65, 22, 86, 22, 86, 22, 72, 20, 77, 38, 79, 20, 88, 18, 65, 59, 76, 25, 92, 26, 66, 18, 76, 48, 93, 19, 89, 33, 84, 28, 113, 20, 66, 128, 98, 84, 18, 28, 76, 128, 77, 76, 19, 78, 22, 73, 20, 68, 25, 73, 19, 83, 23, 103, 28, 24, 68, 20, 65, 19, 74, 32, 78, 19, 67, 18, 71, 26, 89, 19, 67, 23, 75, 24, 80, 27, 70, 19, 69, 40, 70, 19, 66, 23, 124, 29, 81, 58, 65, 19, 87, 18, 82, 27, 89, 20, 82, 20, 88, 33, 91, 19, 90, 24, 78, 22, 70, 49, 77, 128, 169, 85, 38, 70, 18, 72, 128, 98, 18, 73, 18, 65, 30, 87, 51, 129, 139, 70, 22, 65, 26, 87, 23, 68, 51, 92, 20, 72, 128, 87, 91, 19, 121, 21, 82, 31, 66, 22, 68, 20, 70, 27, 91, 20, 69, 18, 75, 26, 68, 21, 192, 189, 33, 68, 20, 80, 33, 71, 19, 97, 24, 69, 21, 90, 20, 65, 37, 102, 20, 103, 128, 64, 89, 18, 85, 36, 67, 18, 87, 25, 124, 33, 80, 24, 92, 49, 66, 33, 20, 26, 99, 128, 77, 90, 24, 73, 22, 73, 21, 67, 18, 87, 25, 74, 33, 83, 23, 84, 21, 86, 23, 90, 42, 88, 128, 69, 66, 20, 127, 24, 70, 27, 114, 25, 68, 27, 102, 19, 74, 28, 73, 18, 98, 31, 84, 26, 81, 19, 90, 20, 73, 31, 73, 23, 80, 32, 76, 18, 192, 65, 54, 98, 128, 68, 79]

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
print (sum(mono_uncomp_roi))
histo = numpy.histogram(mono_uncomp_roi)
print (histo)


for row in range (0,54):
      
        print("  ".join("%3d" %val for val in mono_uncomp_roi [row * 38 : (row + 1) * 38]))


 
    