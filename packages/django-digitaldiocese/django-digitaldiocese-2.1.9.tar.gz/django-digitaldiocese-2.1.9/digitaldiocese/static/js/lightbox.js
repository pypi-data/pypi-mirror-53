var btn = document.getElementsByClassName('item');
var lightbox = document.getElementById('light-box');
var event_details = document.getElementById('event-details');
var event_content = document.getElementById('item-content');
var close_btn = document.getElementById('close-btn');
var detail_holder = document.getElementById('items-list');
lightbox.className = 'hidden';

function deploy_lightbox(el) {
	lightbox.classList.remove('hidden', 'fade-out');
	detail_holder.appendChild(this.parentNode.cloneNode(true));
}

for (var i = 0; i < btn.length; i++) {
    btn[i].addEventListener('click', deploy_lightbox, false);
}

close_btn.onclick=function(e){
	e.preventDefault();
	var details = document.getElementById('item');
	while (detail_holder.childNodes.length > 2) {
	    detail_holder.removeChild(detail_holder.lastChild);
	}
	lightbox.className = 'hidden';
}
