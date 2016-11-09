<?php
namespace Home\Controller;
use Think\Controller;

defined('PAGE_COUNT') or define('PAGE_COUNT', 50);

class SuperController extends Controller {
    private $today;

    protected function _initialize() {
        $this->today = C('TODAY');
//        $this->today = '2016-09-19';
    }

    public function super_down() {
        $count = M('super_wave')->where("direction=-1")->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $list = M('super_wave')
            ->where("direction=-1")
            ->join('left join stocks_info on super_wave.code = stocks_info.code')
            ->field('super_wave.id, super_wave.code, summit_date, cost_date, man_date, name, industry, min, max, percent, cur_per, flag, cost_price, yield_rate')
            ->order('percent')
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display();
    }

    public function down() {
        $count = M('super_wave')->where("cur_per<=-0.2 and direction=1")->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $list = M('super_wave')
            ->where("cur_per<-0.2 and direction=1")
            ->join('left join stocks_info on super_wave.code = stocks_info.code')
            ->field('super_wave.id, super_wave.code, summit_date, cost_date, man_date, name, industry, min, max, percent, cur_per, flag, cost_price, yield_rate')
            ->order('cur_per')
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display();
    }

    public function super_up() {
        $count = M('super_wave')->where("direction=1")->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $list = M('super_wave')
            ->where("direction=1")
            ->join('left join stocks_info on super_wave.code = stocks_info.code')
            ->field('super_wave.id, super_wave.code, summit_date, cost_date, man_date, name, industry, min, max, percent, cur_per, flag, cost_price, yield_rate')
            ->order('percent desc')
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display();
    }

    public function up() {
        $count = M('super_wave')->where("cur_per>=0.2 and direction=-1")->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $list = M('super_wave')
            ->where("cur_per>=0.2 and direction=-1")
            ->join('left join stocks_info on super_wave.code = stocks_info.code')
            ->field('super_wave.id, super_wave.code, summit_date, cost_date, man_date, name, industry, min, max, percent, cur_per, flag, cost_price, yield_rate')
            ->order('cur_per desc')
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display();
    }

    public function flag() {
        $map['id'] = array('IN', I('get.ids'));

        $data['man_date'] = $this->today;
        $data['flag'] = 1;

        $result = M('super_wave')->where($map)->save($data);

        if($result) {
            $this->success('操作成功！');
        } else {
            $this->error('操作失败！');
        }
    }
}