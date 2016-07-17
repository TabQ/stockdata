<?php
namespace Home\Controller;
use Think\Controller;

class DetailController extends Controller {
    public function index($code) {
        if(IS_POST) {
            $params = I('post.');
            extract($params);

            $code = I('get.code');
            !empty($code) && $data['code'] = $code;

            !empty($typeId) && $data['typeId'] = $typeId;
            !empty($cost_price) && $data['cost_price'] = $cost_price;
            !empty($date) && $data['date'] = $date;
            $data['subTypeId'] = 2;     // 手选

            $queryResult = M('focus_pool')->where("code=$code and typeId=$typeId and subTypeId=2")->find();
            if(!empty($queryResult)) {
                $this->ajaxReturn(array('status' => 0, 'msg' => '该类型已经添加过！'));
            }

            $result = M('focus_pool')->data($data)->add();
            if($result) {
                $this->ajaxReturn(array('status' => 1, 'msg' => '操作成功！', 'typeId' => $typeId, 'costPrice' => $cost_price, 'date' => $date));
            } else {
                $this->ajaxReturn(array('status' => 0, 'msg' => '操作失败！'));
            }
        } else {
            $info = M('stocks_info')->where("code=$code")->field('code, name')->find();
            if(empty($info)) {
                $this->error('数据不存在！');
            }

            $list = M('focus_type')->order('id')->select();

            $this->assign('info', $info);
            $this->assign('list', $list);

            $this->display();
        }
    }
}