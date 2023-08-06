class Banner {
    constructor(parent_div_name, message, type, closing_button=true)
    {
        this.parentDiv = $(parent_div_name);
        this.type = type+'-banner';

        this.createBanner(message);
        if(closing_button) {
            this.createCloseButton();
        }
    }

    createBanner(message) {
        $("<div>").attr({'class': '_flexcontainer', 'id': this.type})
            .append($("<span>").attr('class', '_flex').html(message))
            .prependTo(this.parentDiv);
        if (this.canClose) {
            banner_div.append();
            $('#info-banner .close_button').on('click', function () {
            })
        }
    }

    createCloseButton() {
        let bannerDiv = this.parentDiv.children('#'+this.type);
        bannerDiv.append($("<span>").attr('class', '_flexfixedsize _flex-end close_button').text('X'));
        bannerDiv.children('.close_button').on('click', function(){
            bannerDiv.slideUp();
        });
    }
}