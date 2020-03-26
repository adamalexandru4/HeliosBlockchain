
var wizard = $("#example-async");


wizard.steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slide",
    transitionEffectSpeed: 150,
    labels: {
        finish: 'Finish <i class="fa fa-chevron-right"></i>',
        next: 'Next <i class="fa fa-chevron-right"></i>',
        previous: '<i class="fa fa-chevron-left"></i> Previous'
    },
    onStepChanging: function (event, currentIndex, newIndex)
    {
        if(!contractDeployed)
            return false;

        console.log("new");
        return true;
    },
    onStepChanged: function (event, currentIndex, priorIndex)
    {
        console.log("changed");
    },
    onFinishing: function (event, currentIndex) {
        console.log("finishing");
        return true;
    },
    onFinished: function (event, currentIndex)
    {
        alert("Submitted!");
    }
});

