from profile_scholarshipapp.models import Profile_scholarship


def profile_completeness_calculator(user):
    target_profile=user.profile
    profile_instance = {
        '학력': hasattr(target_profile, 'profile_scholarship'),
        '고교 성적': hasattr(target_profile, 'profile_gpa'),
        '수능 성적': target_profile.profile_sat.exists(),
        '경력': target_profile.profile_career.exists(),
        '교과목': target_profile.profile_subject.exists(),
        '담당 수업': hasattr(target_profile, 'profile_consulttype'),
        '사진': hasattr(target_profile, 'profile_profileimage'),
        '자기 소개': hasattr(target_profile, 'profile_introduction'),
    }

    profile_completed = [key for key, value in profile_instance.items() if value]
    profile_uncompleted = [key for key, value in profile_instance.items() if not value]

    ratio = round(len(profile_completed) * 100 / len(profile_instance)) if profile_instance else 0

    return profile_completed, profile_uncompleted, ratio
