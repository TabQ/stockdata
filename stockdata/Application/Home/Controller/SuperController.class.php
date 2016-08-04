<?php
namespace Home\Controller;
use Think\Controller;

defined('PAGE_COUNT') or define('PAGE_COUNT', 50);

class SuperController extends Controller {
    private $today;

    protected function _initialize() {
        $this->today = C('TODAY');
//        $this->today = '2016-08-01';
    }

    public function super_down() {
        $count = M('super_wave')->where("date='$this->today' and direction=-1")->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $list = M('super_wave')
            ->where("date = '$this->today' and direction=-1")
            ->join('left join stocks_info on super_wave.code = stocks_info.code')
            ->field('super_wave.id, super_wave.code, name, industry, min, max, percent, cur_per')
            ->order('percent')
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display();
    }

    public function down() {
        $count = M('super_wave')->where("date='$this->today' and cur_per<=-0.2 and direction=1")->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $list = M('super_wave')
            ->where("date='$this->today' and cur_per<-0.2 and direction=1")
            ->join('left join stocks_info on super_wave.code = stocks_info.code')
            ->field('super_wave.id, super_wave.code, name, industry, min, max, percent, cur_per')
            ->order('cur_per')
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display();
    }

    public function super_up() {
        $count = M('super_wave')->where("date='$this->today' and percent>=0.3 and direction=1")->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $list = M('super_wave')
            ->where("date = '$this->today' and percent>=0.3 and direction=1")
            ->join('left join stocks_info on super_wave.code = stocks_info.code')
            ->field('super_wave.id, super_wave.code, name, industry, min, max, percent, cur_per')
            ->order('percent desc')
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display();
    }

    public function up() {
        $count = M('super_wave')->where("date='$this->today' and cur_per>=0.2 and direction=-1")->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $list = M('super_wave')
            ->where("date='$this->today' and cur_per>=0.2 and direction=-1")
            ->join('left join stocks_info on super_wave.code = stocks_info.code')
            ->field('super_wave.id, super_wave.code, name, industry, min, max, percent, cur_per')
            ->order('cur_per desc')
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display();
    }
}