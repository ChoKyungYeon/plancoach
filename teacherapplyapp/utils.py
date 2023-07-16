def teacherapply_step_calculator(target_user):
    if target_user.state == 'teacher':
        return 'step3'
    else:
        if hasattr(target_user,'teacherapply'):
            if target_user.teacherapply.apply_done:
                return 'step2'
        return 'step1'


