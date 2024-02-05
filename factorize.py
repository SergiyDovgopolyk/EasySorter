import time
from multiprocessing import Pool, cpu_count


def factorize(*number: int) -> list[list, ...]:
    results = []
    for num in number:
        i = 1
        result = []
        while i ** 2 <= num:
            if num % i == 0:
                result.append(i)
                if num != num // i:
                    result.append(num // i)
            i += 1
        result.sort()
        result.append(num)
        results.append(result)
    return results


def factorize_slow(*number: int) -> list[list, ...]:
    results = []
    for num in number:
        i = 1
        result = []
        while i <= num:
            if num % i == 0:
                result.append(i)
            i += 1
        results.append(result)
    return results


def mathmatics(number: int) -> list[int]:
    i = 1
    result = []
    while i ** 2 <= number:
        if number % i == 0:
            result.append(i)
            if number != number // i:
                result.append(number // i)
        i += 1
    result.sort()
    result.append(number)
    return result


def mathmatics_slow(number: int) -> list[int]:
    i = 1
    result = []
    while i <= number:
        if number % i == 0:
            result.append(i)
        i += 1
    return result


def callback(result):
    print(f'With process {result}')


def factorize_process(*number: int) -> None:
    with Pool(cpu_count()) as pool:
        pool.map_async(mathmatics, number, callback=callback)
        pool.close()
        pool.join()


def factorize_slow_process(*number: int) -> None:
    with Pool(cpu_count()) as pool:
        pool.map_async(mathmatics_slow, number, callback=callback)
        pool.close()
        pool.join()


if __name__ == '__main__':
    start = time.time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    end = time.time()
    print(a, b, c, d)
    print(f'Fast function {end - start}\n')
    start_slow = time.time()
    a_slow, b_slow, c_slow, d_slow = factorize_slow(128, 255, 99999, 10651060)
    end_slow = time.time()
    print(a_slow, b_slow, c_slow, d_slow)
    print(f'Slow function {end_slow - start_slow}\n')
    start_process = time.time()
    factorize_process(128, 255, 99999, 10651060)
    end_process = time.time()
    print(f'Fast function with process {end_process - start_process}\n')
    start_slow_process = time.time()
    factorize_slow_process(128, 255, 99999, 10651060)
    end_slow_process = time.time()
    print(f'Slow function with process {end_slow_process - start_slow_process}')
