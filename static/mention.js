function mention(mentionedPostId) {
  var body = $("#body");
  body.val(body.val() + `>>${mentionedPostId}`);
}
var list = $("p:contains('>>')")
for (i=0; i < list.text().split(' ').length; i++){
    if (list.text().split(' ')[i].substring(0,2) == '>>'){
        console.log('found')
        const id = list.text().split(' ')[i]
        list.text(list.text().replace(id, ' '));
        list.prepend(`<a href="#${id.replace('>>', '')}">${id}</a>`)
    }
}