<?php
namespace Home\Controller;
use Think\Controller;

class DetailController extends Controller {
    public function index($code) {
        if(IS_POST) {
            $params = I('post.');
            extract($params);

            $data['code'] = $code;

            !empty($type_id) && $data['type_id'] = $type_id;
            !empty($cost_price) && $data['cost_price'] = $cost_price;
            !empty($date) && $data['date'] = $date;
            $data['subtype_id'] = 2;     // 手选
            $data['man_date'] = C('TODAY');     // 手选操作日期

            // 删除已存在数据
            $idsArr = M('focus_pool')->where("code='$code'")->getField('id', true);
            if(!empty($idsArr)) {
                $where['id'] = array('in', $idsArr);
                M('focus_pool')->where($where)->delete();
            }

            // 添加新记录
            $id = M('focus_pool')->data($data)->add();
            // 如果成本价未填写则以当日收盘价为准
            if(empty($cost_price) && !empty($date)) {
                $map['date'] = $date;
                $map['code'] = $code;
                $getCostPrice = M('k_data')->where($map)->getField('close');

                M('focus_pool')->where("id=$id")->setField('cost_price', $getCostPrice);
            }
            if($id) {
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