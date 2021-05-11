$(document).ready(function () {
    let netNum = 0;
    let nextNode = 0;
    $("button").click(function () {
        nextNode++;
        $("#test").load("load-test.php", {
            net: netNum,
            nextNode: nextNode,
            test: 'NO4254wre32T NICK'
        });
    });
});