<?php
namespace Home\Controller;
use Think\Controller;

defined('PAGE_COUNT') or define('PAGE_COUNT', 50);

class IndexController extends Controller {
    private $today;

    protected function _initialize() {
        $this->today = C('TODAY');
    }

    public function __call($name, $arguments) {
        $params = I('get.');
        extract($params);

        $map['focus_pool.date'] = array('elt', $this->today);
        !empty($typeid) && $map['typeId'] = $typeid;
        !empty($subtypeid) && $map['subTypeId'] = $subtypeid;

        $count = M('focus_pool')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $sort = $name == 'index' ? 'yield_rate desc' : ($desc == 1 ? "$name desc" : "$name");

        $list = M('focus_pool')
            ->where($map)
            ->join('left join stocks_info on focus_pool.code = stocks_info.code')
            ->join('left join perday_info on focus_pool.code = perday_info.code and focus_pool.date = perday_info.date')
            ->field('focus_pool.id, focus_pool.code, focus_pool.date, count, latest, man_date, typeId, subTypeId, cost_price, yield_rate, name, industry, p_change, v2ma20, vma20_2_max, turnover, timetomarket')
            ->order($sort)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $typeList = M('focus_type')->order('id')->select();

        $this->assign('type_list', $typeList);
        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Index:index');
    }

    public function delete() {
        $map['id'] = array('IN', I('get.ids'));

        M('focus_pool')->where($map)->delete();

        $this->redirect('Index/index');
    }
}