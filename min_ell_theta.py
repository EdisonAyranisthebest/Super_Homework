def learn_theta(data, colors):
    '''
    Finds theta that is larger than all blue and less than all red.
    '''
    max_blue = float('-inf')
    min_red = float('inf')

    for x, c in zip(data, colors):
        if c == 'blue':
            if x > max_blue:
                max_blue = x
        else:  
            if x < min_red:
                min_red = x

    return (max_blue + min_red) / 2.0


def compute_ell(data, colors, theta):
    '''
    Computes the loss function L(theta) for a given theta.
    '''
    loss = 0
    for x, c in zip(data, colors):
        if c == 'red' and x <= theta:
            loss += 1
        elif c == 'blue' and x > theta:
            loss += 1
    return float(loss)


def minimize_ell(data, colors):
    '''
    Finds theta that minimizes the loss function L(theta) using quadratic time complexity.
    '''
    best_theta = None
    best_loss = float('inf')

    for x in data:
        theta = x
        loss = compute_ell(data, colors, theta)
        if loss < best_loss:
            best_loss = loss
            best_theta = theta

    return best_theta


def minimize_ell_sorted(data, colors):
    '''
    Finds theta that minimizes the loss function L(theta) in linear time.
    '''
    n = len(data)
    total_blue = sum(1 for c in colors if c == 'blue')

    red_so_far = 0
    blue_so_far = 0

    best_theta = data[0]
    best_loss = float('inf')

    for i in range(n):
        if colors[i] == 'red':
            red_so_far += 1
        else:  # 'blue'
            blue_so_far += 1

        blue_gt_theta = total_blue - blue_so_far
        loss = red_so_far + blue_gt_theta

        if loss < best_loss:
            best_loss = loss
            best_theta = data[i]

    return best_theta
