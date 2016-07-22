<?php
namespace Home\Controller;
use Think\Controller;

class DetailController extends Controller {
    public function index($code) {
        if(IS_POST) {
            $params = I('post.');
            extract($params);

            $data['code'] = $code;

            !empty($typeId) && $data['typeId'] = $typeId;
            !empty($cost_price) && $data['cost_price'] = $cost_price;
            !empty($date) && $data['date'] = $date;
            $data['subTypeId'] = 2;     // 手选
            $data['man_date'] = C('TODAY');     // 手选操作日期

            // 删除已存在数据
            $idsArr = M('focus_pool')->where("code='$code'")->getField('id', true);
            if(!empty($idsArr)) {
                $where['id'] = array('in', $idsArr);
                M('focus_pool')->where($where)->delete();
            }

            // 添加新记录
            $result = M('focus_pool')->data($data)->add();
            if($result) {
                $this->ajaxReturn(array('status' => 1, 'msg' => '操作成功！'));
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