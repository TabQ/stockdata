<?php
namespace Home\Controller;
use Think\Controller;

defined('PAGE_COUNT') or define('PAGE_COUNT', 50);

class PerdayController extends Controller {
    private $today;

    protected function _initialize() {
        $this->today = C('TODAY');
    }

    public function up() {
        $params = I('get.');
        extract($params);

        $lastData = M('up_down')->field('date')->order('date desc')->limit(1)->find();
        $lastDay = $lastData['date'];
        $map['up_down.date'] = array('eq', $lastDay);

        $map['percent'] = array('egt', 2.00);

        if(!empty($range)) {
            switch($range) {
                case 1:
                    $map['percent'] = array('egt', 8.00);
                    break;
                case 2:
                    $map['percent'] = array(array('egt', 5.00), array('lt', 8.00));
                    break;
                case 3:
                    $map['percent'] = array(array('egt', 2.00), array('lt', 5.00));
                    break;
                default:
                    break;
            }
        }

        $count = M('up_down')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $order = !isset($sort) ? 'percent desc' : ($desc == 1 ? "$sort desc" : "$sort");

        $list = M('up_down')
            ->where($map)
            ->join('left join volume_break on up_down.code = volume_break.code and up_down.date = volume_break.date')
            ->join('left join k_data on up_down.code = k_data.code and up_down.date = k_data.date')
            ->join('left join stocks_info on up_down.code = stocks_info.code')
            ->join('left join stocks_report on up_down.code = stocks_report.code')
            ->join('left join stocks_growth on up_down.code = stocks_growth.code')
            ->field('name, up_down.code, up_down.date, percent, v2ma5, v2ma20, close, industry, pe, timetomarket, stocks_info.bvps, profits_yoy, mbrg')
            ->order($order)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Perday:up');
    }

    public function down() {
        $params = I('get.');
        extract($params);

        $lastData = M('up_down')->field('date')->order('date desc')->limit(1)->find();
        $lastDay = $lastData['date'];
        $map['up_down.date'] = array('eq', $lastDay);

        $map['percent'] = array('elt', -2.00);

        if(!empty($range)) {
            switch($range) {
                case 1:
                    $map['percent'] = array('elt', -8.00);
                    break;
                case 2:
                    $map['percent'] = array(array('gt', -8.00), array('elt', -5.00));
                    break;
                case 3:
                    $map['percent'] = array(array('gt', -5.00), array('elt', -2.00));
                    break;
                default:
                    break;
            }
        }

        $count = M('up_down')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $order = !isset($sort) ? 'percent' : ($desc == 1 ? "$sort desc" : "$sort");

        $list = M('up_down')
            ->where($map)
            ->join('left join volume_break on up_down.code = volume_break.code and up_down.date = volume_break.date')
            ->join('left join k_data on up_down.code = k_data.code and up_down.date = k_data.date')
            ->join('left join stocks_info on up_down.code = stocks_info.code')
            ->join('left join stocks_report on up_down.code = stocks_report.code')
            ->join('left join stocks_growth on up_down.code = stocks_growth.code')
            ->field('name, up_down.code, up_down.date, percent, v2ma5, v2ma20, close, industry, pe, timetomarket, stocks_info.bvps, profits_yoy, mbrg')
            ->order($order)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Perday:down');
    }
}