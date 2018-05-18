#coding:utf-8
import itchat
import time
from itchat.content import TEXT
from itchat.content import FRIENDS
itchat.auto_login(hotReload=True,enableCmdQR=2)
dict={}
#返回最新的新字典数据
def updateRooms():
	rooms=itchat.get_chatrooms(update=True)[0:]
	my_rdict={}
	for i,room in  zip(range(0,len(rooms)),rooms[0:]):
		my_rdict[i]={'roomname':room['UserName'],'nickname':room['NickName']}
		if my_rdict[i]['nickname']=='':
			my_rdict[i]['nickname']=('群聊(%d)'%i)
	return my_rdict
#获取指定群聊的好友成员信息	
def get_friendsInfo_in_room(chatRoomName,memberlist):
	friendInRoom='%s(%d人)\n'%(chatRoomName,len(memberlist['MemberList']))
	count=0
	for user in memberlist['MemberList']:
		if (user['ContactFlag']!=0):
			count+=1
			#print("nickname:%s DisplayName:%s"%(user['NickName'],user['DisplayName']))
			friendInRoom+="[好友%d]nickname:%s DisplayName:%s 备注:%s\n\n"%(count,user['NickName'],user['DisplayName'],user['RemarkName'])
	friendInRoom+='该群共有%d好友'%(count)
	return friendInRoom

#获取好友信息
def get_friendsInfo(memberlist):
	for user in memberlist['MemberList']:
			#print("nickname:%s DisplayName:%s"%(user['NickName'],user['DisplayName']))
			friendInRoom+="[好友%d]nickname:%s DisplayName:%s 备注:%s\n\n"%(count,user['NickName'],user['DisplayName'],user['RemarkName'])
	friendInRoom+='该群共有%d好友'%(len(memberlist))

#向特定的群好友发定制的信息				
def send_msg_to_room_friends(title,message,toFriendsList):
	sendmsg=title+':\n'+message+'\n'+time.asctime(time.localtime(time.time()))
	print(sendmsg)
	for user in toFriendsList['MemberList']:
		 if (user['ContactFlag']!=0):
			 #print("sendto=nickname:%s DisplayName:%s"%(user['NickName'],user['DisplayName' ]))
			 itchat.send(sendmsg,toUserName=user['UserName'])
#处理无参数指令
def cmd_single_deal(cmd):
	print(cmd)
	global dict
	if(cmd=='update' or cmd=='4'):
			dict.clear()
			dict=updateRooms()
			return "update %d datas finish"%len(dict)
	if(cmd=='SendMode' or cmd=='1'):
			rooms_info='查看群聊id:\n'
			for i in  range(0,len(dict)):
				rooms_info+=str(i)+': '+dict[i]['nickname']+'\n'
			return rooms_info
	if(cmd=='help' or cmd=='5'):
			usage='''群好友助手指令：
		1.[SendMode] or 1:查看群id
		2.[SendMode id]:查看指定id群的好友人数
		3.[SendMode 参数0(群id) text 参数a(标题) 参数b(内容)]
		4.[update] or 4:更新数据
		5.[help] or 5:帮助信息
		[注意:参数间只能有一个空格]'''
			return usage	
	return '无效指令！'
#含参数指令处理	
def cmd_with_args_deal(command):
	id=int(command[1])
	
	room_member=itchat.update_chatroom(dict[id]['roomname'],detailedMember=True)

	if((command[0]=='SendMode') and len(command)==2):
				#print('#############%s'%dict[id]['nickname'])
				friendsInRoomInfo=get_friendsInfo_in_room(dict[id]['nickname'],room_member)
				itchat.send(friendsInRoomInfo,toUserName='filehelper')      
	if((command[0]=='SendMode' or command[0]=='1' ) and len(command)==5):
		if(command[2]=='text'):#2:gid 3:title 4:msg
					send_msg_to_room_friends(command[3],command[4],room_member)
#微信响应函数							
@itchat.msg_register([TEXT])
def handel_recive(msg):
	global dict
	if(msg['ToUserName']=='filehelper'):
		command=msg['Content'].split(' ')
		command_len=len(command)
		dict=updateRooms()
		rooms_sum=len(dict)
		if(command_len==1):
			info=cmd_single_deal(command[0])
			itchat.send(info,toUserName='filehelper')
		elif(command_len>1 and command[1].isnumeric()):
			if(int(command[1])<rooms_sum):
				    cmd_with_args_deal(command) 
		else:
		    itchat.send("无效参数",toUserName='filehelper')
		print("send finish!")
		
itchat.send("群好友助手已启动,help指令查看详细说明!",toUserName='filehelper')
itchat.run()
