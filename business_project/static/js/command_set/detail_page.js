const toggleVoteBtns = () => {
    let upvoteNum = parseInt($('#upvote-num').text());
    // If a button is clicked, disable the button and make the other button clickable
    $('.btn-primary').click(function() {
        $(this).addClass('disabled');
        if ($('.btn-danger').hasClass('disabled')) {
            $('.btn-danger').removeClass('disabled');
            upvoteNum = upvoteNum + 2
            $('#upvote-num').text(upvoteNum);
        } else {
            upvoteNum = upvoteNum + 1
            $('#upvote-num').text(upvoteNum);
        }
    })

    $('.btn-danger').click(function() {
        $(this).addClass('disabled');
        if ($('.btn-primary').hasClass('disabled')) {
            $('.btn-primary').removeClass('disabled');
            upvoteNum = upvoteNum - 2;
            $('#upvote-num').text(upvoteNum);
        } else {
            upvoteNum = upvoteNum - 1;
            $('#upvote-num').text(upvoteNum);
        }
    })
}

toggleVoteBtns();