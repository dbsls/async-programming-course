from gc import disable as gc_disable, enable as gc_enable


def count_words(lines: list[str]):
    words = {}
    for line in lines:
        _word, _, match_count, _ = line.split("\t")
        if _word in words:
            words[_word] += int(match_count)
        else:
            words[_word] = int(match_count)
    return words


def mp_count_words(lines: list[str], counter, lock):
    # words_num = 0
    # step = 100
    words = {}
    for line in lines:
        _word, _, match_count, _ = line.split("\t")
        if _word in words:
            words[_word] += int(match_count)
        else:
            words[_word] = int(match_count)

        # monitoring
        # because of lock, this can slow down processing time
        #
        # words_num += 1
        # if words_num % step == 0:
        #     words_num = 0
        #         counter.value += step

    with lock:
        counter.value += len(lines)
    return words


def process_file_chunk(
    file_name: str,
    chunk_start: int,
    chunk_end: int,
    counter,
    lock,
) -> dict:
    """Process each file chunk in a different process"""
    diff = chunk_end - chunk_start
    words = dict()
    with open(file_name, mode="r") as f:
        f.seek(chunk_start)
        gc_disable()
        for line in f:
            chunk_start += len(line)
            if chunk_start > chunk_end:
                break
            _word, _, match_count, _ = line.split("\t")
            if _word in words:
                words[_word] += int(match_count)
            else:
                words[_word] = int(match_count)
        with lock:
            counter.value += diff
        gc_enable()
    return words
