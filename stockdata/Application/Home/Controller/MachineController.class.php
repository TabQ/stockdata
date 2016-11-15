<?php
namespace Home\Controller;
use Think\Controller;

defined('PAGE_COUNT') or define('PAGE_COUNT', 50);

class MachineController extends Controller {
    private $today;

    protected function _initialize() {
        $this->today = C('TODAY');
    }

    public function __call($name, $arguments) {
        $params = I('get.');
        extract($params);

        $subQuery = M('action_log')->where('action_id = 13')->field("from_unixtime(time, '%Y-%m-%d') as date")->buildSql();
        $condition = "type_id = 1 and subtype_id = 1 and focus_pool.date not in $subQuery";

        $count = M('focus_pool')->where($condition)->order('date desc')->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $sort = $name == 'index' ? 'date' : ($desc == 1 ? "$name desc" : "$name");

        $list = M('focus_pool')
            ->where($condition)
            ->join('left join stocks_info on focus_pool.code = stocks_info.code')
            ->join('left join k_data on focus_pool.code = k_data.code and focus_pool.date = k_data.date')
            ->field('focus_pool.id, focus_pool.code, focus_pool.date, count, latest, cost_price, yield_rate, name, industry, timetomarket')
            ->order($sort)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Machine:index');
    }

    public function delete() {
        $map['id'] = array('IN', I('get.ids'));

        $result = M('focus_pool')->where($map)->delete();

        if($result) {
            $this->success('操作成功！');
        } else {
            $this->error('操作失败！');
        }
    }

    public function manual() {
        $subQuery = M('action_log')->where('action_id = 13')->field("from_unixtime(time, '%Y-%m-%d') as date")->buildSql();
        $condition = "typeId = 1 and subTypeId = 1 and focus_pool.date not in $subQuery";

        $dateArr = M('focus_pool')->where($condition)->distinct(true)->getField('date', true);
        foreach($dateArr as $value) {
            $timeStamp = strtotime($value . ' 20:00:00');
            $dataList[] = array('action_id' => 13, 'time' => $timeStamp);
        }

        if(!empty($dataList)) {
            $result = M('action_log')->addAll($dataList);
        } else {
            $data['action_id'] = 13;
            $data['time'] = strtotime($this->today . ' 20:00:00');

            $result = M('action_log')->add($data);
        }

        if($result) {
            $this->ajaxReturn(array('status' => 1, 'msg' => '操作成功！'));
        } else {
            $this->ajaxReturn(array('status' => 1, 'msg' => '操作失败！'));
        }
    }
}