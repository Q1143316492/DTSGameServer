

if __name__ == '__main__':
    sum = [0 for v in range(200)]

    while True:
        a = raw_input().split()
        if len(a) == 1:
            break
        t = int(a[0]) / 10
        cnt = int(a[1])
        sum[t] += cnt

    for i in range(0, len(sum)):
        if sum[i] == 0:
            continue
        print i, sum[i]