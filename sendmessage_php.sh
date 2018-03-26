#!/usr/bin/php

<?php
mb_language("uni");
mb_internal_encoding("UTF-8");
require('/usr/lib/zabbix/alertscripts/PHPMailer-master/PHPMailerAutoload.php');

$MAIL_LOG_PATH = '/var/log/zabbix-phpmailer'; //日志
$MAIL_FROM = "xxxxxxx@xxx.com"; //邮件的from信息
$MAIL_FROMNAME = "Zabbixtest 障害通知"; //邮件的from信息
$MAIL_SMTP_HOST = 'smtp.partner.outlook.cn:587'; //邮箱的host信息（ssl）
$MAIL_SMTP_USER = ' xxxxxxx@xxx.com '; //用户名
$MAIL_SMTP_PASS = 'xxxxxxx'; //密码
$retry_count = 3; //重试3次

//邮件的TO，CC从文件中取得，文件名为第一个参数
$MAIL_LIST_NM = $argv[1];
$MAIL_LIST = '/usr/lib/zabbix/alertscripts/addresslist/'.$MAIL_LIST_NM;
$MAIL_ADRESS = file_get_contents($MAIL_LIST);
$ADRESS_ARRAY = array();
$ADRESS_ARRAY = explode('##',$MAIL_ADRESS);
$MAIL_TO = $ADRESS_ARRAY[0];
$MAIL_CC = $ADRESS_ARRAY[1];

//邮件的标题和内容为第二，第三个参数
$MAIL_SUBJECT = $argv[2];
$MAIL_MESSAGE = $argv[3];
$mailer = new PHPMailer();
$mailer->CharSet = 'UTF-8';
$mailer->Encoding = 'base64';
$mailer->IsSMTP();
$mailer->SMTPSecure='tls';
$mailer->Host = $MAIL_SMTP_HOST;
$mailer->SMTPAuth = true;
$mailer->Username = $MAIL_SMTP_USER;
$mailer->Password = $MAIL_SMTP_PASS;
$mailer->From = $MAIL_FROM;

//to,cc,bcc edit
$TO_COUNT = array();
$CC_COUNT = array();
$TO_COUNT = explode(',',$MAIL_TO);
$CC_COUNT = explode(',',$MAIL_CC);
$key;

while ($key = current($TO_COUNT)) {
$mailer->AddAddress($key);
next($TO_COUNT);
}

 

while ($key = current($CC_COUNT)) {
$mailer->AddCC($key);
next($CC_COUNT);
}

$mailer->FromName = mb_convert_encoding($MAIL_FROMNAME,"UTF-8","UTF-8");
$mailer->Subject = $MAIL_SUBJECT;
$mailer->Body = mb_convert_encoding($MAIL_MESSAGE,"UTF-8","UTF-8");

/* logging data set */
$queuing_time = explode(' ', microtime());
$queuing_id = date('YmdHis', $queuing_time[1]).' '.$queuing_time[0];
$log_sub_dir = $MAIL_LOG_PATH;
$log_filename = $log_sub_dir .'/'.substr($queuing_id, 0, 8).'.txt';
$log_message = "From: $MAIL_FROM\n";
$log_message .= "To: $MAIL_TO\n";
$log_message .= "Subject: $MAIL_SUBJECT\n";
$log_message .= "Message: $MAIL_MESSAGE\n";
$retry = 0;

/* mail info */
$mail_info = ' to send mail to ';
$mail_info .= $MAIL_LIST_NM;
$mail_info .='(';
$mail_info .= 'Subject:'.$MAIL_SUBJECT;
$mail_info .= ' To:'.str_replace("\n","",$MAIL_TO);
$mail_info .= ' Cc:'.str_replace("\n","",$MAIL_CC);
$mail_info .= ' Message:'.str_replace("\n","←",$MAIL_MESSAGE);
$mail_info .=')';

//如果失败，重试3次
do{
try {
$send_result=$mailer->Send();
} catch (Exception $e) {
Logging($log_sub_dir, $log_filename, $queuing_id.'['.$retry.']', 'Exception:'.$e->getMessage()."\n");
$send_result=false;
}

if(!$send_result){
Logging($log_sub_dir, $log_filename, $queuing_id.'['.$retry.']', 'Result: failed '.$mailer->ErrorInfo."\n".$log_message);
print 'failed: ' . $mailer->ErrorInfo . "\n";
}else{
Logging($log_sub_dir, $log_filename, $queuing_id.'['.$retry.']', "Result: success\n".$log_message);
print 'success' . "\n";
break;
}

$retry++;
sleep(10);
$log_message = '';
}while ($retry < $retry_count);

if($retry==$retry_count){
OutputResult($log_sub_dir,$log_sub_dir.'/mailresult.log', 'outlook failed'.$mail_info);
}else{
OutputResult($log_sub_dir,$log_sub_dir.'/mailresult.log', 'outlook success'.$mail_info);
}

/* logging */
function Logging($dir, $filename, $id, $message) {
if (!is_dir($dir)) { mkdir($dir, 0755); }
$logging_time = explode(' ', microtime());
$logging_date = date('YmdHis', $logging_time[1]).' '.$logging_time[0];
$log = '----- Logging Date: '.$logging_date."\n";
$log.= 'Queuing ID: '.$id."\n";
$log.= $message."\n";
$fp = fopen($filename, 'a');
fwrite($fp, $log);
fclose($fp);
}

function OutputResult($dir, $filename, $info) {
if (!is_dir($dir)) { mkdir($dir, 0755); }
$logging_time = explode(' ', microtime());
$logging_date = date('YmdHis', $logging_time[1]);
$log = $logging_date.':'.$info."\n";
$fp = fopen($filename, 'a');
fwrite($fp, $log);
fclose($fp);
}

?>