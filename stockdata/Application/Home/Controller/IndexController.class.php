<?php
namespace Home\Controller;
use Think\Controller;

defined('PAGE_COUNT') or define('PAGE_COUNT', 50);

class IndexController extends Controller {
    private $today = '2016-02-16';

    public function index() {
        $count = M('focus_pool')->where("focus_pool.date < '$this->today' and typeId = 1")->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $list = M('focus_pool')
            ->where("focus_pool.date < '$this->today' and typeId = 1")
            ->join('left join stocks_info on focus_pool.code = stocks_info.code')
            ->join('left join perday_info on focus_pool.code = perday_info.code and focus_pool.date = perday_info.date')
            ->field('focus_pool.id, focus_pool.code, focus_pool.date, count, other_date, typeId, subTypeId, yield_rate, name, industry, close, p_change, v2ma20, vma20_2_max, turnover, timetomarket')->order('yield_rate desc')->limit($page->firstRow.','.$page->listRows)->select();

        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Index:index');
    }

    public function __call($name, $arguments) {
        $count = M('focus_pool')->where("focus_pool.date < '$this->today' and typeId = 1")->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $sort = I('get.desc') ? ' desc' : '';
        $list = M('focus_pool')
            ->where("focus_pool.date < '$this->today' and typeId = 1")
            ->join('left join stocks_info on focus_pool.code = stocks_info.code')
            ->join('left join perday_info on focus_pool.code = perday_info.code and focus_pool.date = perday_info.date')
            ->field('focus_pool.id, focus_pool.code, focus_pool.date, count, other_date, typeId, subTypeId, yield_rate, name, industry, close, p_change, v2ma20, vma20_2_max, turnover, timetomarket')->order("$name$sort")->limit($page->firstRow.','.$page->listRows)->select();

        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Index:index');
    }

    public function delete() {
        $map['id'] = array('IN', I('get.ids'));

        M('focus_pool')->where($map)->delete();

        $this->index();
    }
}