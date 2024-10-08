
import htmx from "htmx.org";


const modalSelector = "#modal-slide";


// close modal on overlay click
document.addEventListener("modalSlide:close", function (event) {
    let modalElt = htmx.find(modalSelector);
    modalElt.innerHTML = "";
    modalElt.classList.remove('modal-overlay-show');
});



htmx.defineExtension("modal-slide", {

    onEvent: function (name, evt) {
        // console.log(name, evt); 
        if (name === "htmx:trigger") {
            let modalElt = htmx.find(modalSelector);
            modalElt.classList.add('modal-overlay-show');
            document.body.classList.add('cursor-wait');
        }

        if (name === "htmx:beforeOnLoad") {
            // console.log(name, evt); 
            document.body.classList.remove('cursor-wait');
            
            // add wrapper div, which becomes the target
            let content = document.createElement('div');
            content.className = 'modal-slide-content';
            content.setAttribute('hx-target', 'this');
            
            let modalElt = htmx.find(modalSelector);
            modalElt.appendChild(content);

            // re-target
            evt.detail.target = content;
        }

        return true
    },


});