function showTeacherSlide() {
    // Change the class of the teacher button
    document.querySelector('.item1_teacher_button').classList.add('Body_item_touched');
    document.querySelector('.item1_teacher_button').classList.remove('Body_item_nottouched');

    // Change the class of the student button
    document.querySelector('.item1_student_button').classList.add('Body_item_nottouched');
    document.querySelector('.item1_student_button').classList.remove('Body_item_touched');

    // Hide the student slide
    document.querySelector('#item1_student_slide').style.display = 'none';

    // Show the teacher slide
    document.querySelector('#item1_teacher_slide').style.display = 'block';
}