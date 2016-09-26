(function() {
    Galleria.loadTheme('js/lib/galleria/galleria.classic.min.js');
    Galleria.configure({
        showInfo:false,
        showImagenav:false,
        imageCrop:true,
        autoplay:4000,
        thumbFit:true,
        thumbCrop:true,
        thumbMargin:1,
        height: 0.9
    })
    Galleria.run('.galleria');
    // $(".galleria-container").css("height","440px");
}());