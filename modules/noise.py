import random


# Generating list of normal distributed values (gaussian distributed)
def generate_noise(mean,std,n):
    noise =[]
    for i in range(n):
        noise.append(random.gauss(mean, std))
    return noise

# applying noise to signal
# signal and noise must be the same length
def received_sig (sig,noise):
    rx_sig = []
    for i in range(0,len(sig)):
        rx_sig.append(sig[i]+noise[i])
    return rx_sig

# detecting signal
def detected_sig(received_sig):
    det_sig = []
    for i in range(0,len(received_sig)):
        det_sig.append(2 * (received_sig[i] >= 0) - 1)
    return det_sig

# calculating error between 2 signals
def err(detected_sig,transmited_sig):
    cnt = 0
    for i in range(0,len(transmited_sig)):
        cnt += 1 * (transmited_sig[i] != detected_sig[i])

    return cnt

def print_info(snrindB,no_errors,ber):
    print("SNR in dB:", snrindB)
    print("Numbder of errors:", no_errors)
    print("Error probability:", ber)