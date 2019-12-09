# 記帳貓咪


## Setup

### Prerequisite
* Python 3
* LineBOT

#### Install Dependency
```sh
pip3 install -r requirements.txt
```



#### Run the sever

```sh
python3 app.py
```

#### b. Servo

Or You can use [servo](http://serveo.net/) to expose local servers to the internet.


## Finite State Machine
![fsm](./fsm.png)

## Usage
The initial state is set to `user`.

Every time `user` state is triggered to `advance` to another state, it will `go_back` to `user` state after the bot replies corresponding message.

* user
	* Input: "記帳"
		* Reply: ""

	* Input: "我的帳本"
		* Reply: "喵哈哈!!來看看你都花了多少錢吧~\n餐費:\n娛樂費:\n交通費:\n其他:\n總支出:"

## Deploy
Setting to deploy webhooks on Heroku.




