
var editor;

window.onload = function() {
    editor  = new MediumEditor('body p', {autolink: true});


    editor.subscribe('focus', function(data, editable) { if (!editable.hasAttribute('data-original')) {
    editable.dataset.original = editable.innerText};
                                                       });

    editor.subscribe('blur', function(data, editable) {
    old_html = editable.dataset.original;
    new_html = editable.innerHTML;
    if (old_html == new_html) {
        return;
    }
    index = editable.dataset.mediumEditorEditorIndex;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'https://cors-anywhere.herokuapp.com/https://editable-docs-bot.herokuapp.com/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    data = {
        index: index,
        old_html: old_html,
        new_html: new_html,
        rendered_html_url: document.URL,
        rendered_rst_url: document.evaluate('//a[@class="fa fa-github"]', document, null, XPathResult.ANY_TYPE, null).iterateNext().href
   };
   xhr.send(JSON.stringify(data))});


}
