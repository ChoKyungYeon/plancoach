def solution(land):
    row_length=len(land[0])
    column_length=len(land)
    answer_list = [0] * row_length
    def sum_sections(binary_list):
        sum = 0
        result = []
        for num in binary_list:
            if num == 1:
                sum += 1
            else:
                if sum > 0:
                    result.extend([sum] * sum)
                    sum = 0
                result.append(0)
        if sum > 0:
            result.extend([sum] * sum)
        return result

    for i in range(column_length):
        print(i,answer_list)
        answer_list=[a + b for a, b in zip(answer_list, sum_sections(land[i]))]



    answer = max(answer_list)
    return answer

print(solution(
    [[0, 0, 0, 1, 1, 1, 0, 0],
     [0, 0, 0, 0, 1, 1, 0, 0],
     [1, 1, 0, 0, 0, 1, 1, 0],
     [1, 1, 1, 0, 0, 0, 0, 0],
     [1, 1, 1, 0, 0, 0, 1, 1]
     ]))