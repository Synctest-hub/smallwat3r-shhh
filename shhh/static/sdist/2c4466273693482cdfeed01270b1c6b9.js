
$(document).ready(function(){$('#secretSender').on('submit',function(event){event.preventDefault();blockUI();$.ajax({url:'/api/send',data:$('#secretSender').serialize(),type:'POST',success:function(d){$('#linkPop').fadeIn(1000);$('#linkDetail').empty().append(window.location.host+'/read?slug='+d.slug);$('#linkExpire').empty().append(d.expires);},complete:function(){$.unblockUI();}});});});