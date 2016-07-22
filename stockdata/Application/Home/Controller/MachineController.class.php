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
        $condition = "typeId = 1 and subTypeId = 1 and focus_pool.date not in $subQuery";

        $count = M('focus_pool')->where($condition)->order('date desc')->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $sort = $name == 'index' ? 'date' : ($desc == 1 ? "$name desc" : "$name");

        $list = M('focus_pool')
            ->where($condition)
            ->join('left join stocks_info on focus_pool.code = stocks_info.code')
            ->join('left join perday_info on focus_pool.code = perday_info.code and focus_pool.date = perday_info.date')
            ->field('focus_pool.id, focus_pool.code, focus_pool.date, count, latest, cost_price, yield_rate, name, industry, p_change, v2ma20, vma20_2_max, turnover, timetomarket')
            ->order($sort)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Machine:index');
    }

    public function delete() {
        $map['id'] = array('IN', I('get.ids'));

        M('focus_pool')->where($map)->delete();

        $this->redirect('Machine/index');
    }

    public function manual() {
        $subQuery = M('action_log')->where('action_id = 13')->field("from_unixtime(time, '%Y-%m-%d') as date")->buildSql();
        $condition = "typeId = 1 and subTypeId = 1 and focus_pool.date not in $subQuery";

        $dateArr = M('focus_pool')->where($condition)->distinct(true)->getField('date', true);
        foreach($dateArr as $value) {
            $timeStamp = strtotime($value . ' 20:00:00');
            $dataList[] = array('action_id' => 13, 'time' => $timeStamp);
        }

        !empty($dataList) && $result = M('action_log')->addAll($dataList);
        if($result) {
            $this->ajaxReturn(array('status' => 1, 'msg' => '操作成功！'));
        } else {
            $this->ajaxReturn(array('status' => 1, 'msg' => '操作失败！'));
        }
    }
}