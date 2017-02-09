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

        $lastData = M('stocks_extends')->field('date')->order('date desc')->limit(1)->find();
        $lastDay = $lastData['date'];
        $map['stocks_extends.date'] = array('eq', $lastDay);

        $map['stocks_extends.type'] = 'S';
        $map['p_change'] = array('egt', 2.00);

        if(!empty($range)) {
            switch($range) {
                case 1:
                    $map['p_change'] = array('egt', 8.00);
                    break;
                case 2:
                    $map['p_change'] = array(array('egt', 5.00), array('lt', 8.00));
                    break;
                case 3:
                    $map['p_change'] = array(array('egt', 2.00), array('lt', 5.00));
                    break;
                default:
                    break;
            }
        }

        $count = M('stocks_extends')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $order = !isset($sort) ? 'p_change desc' : ($desc == 1 ? "$sort desc" : "$sort");

        $list = M('stocks_extends')
            ->where($map)
            ->join("left join volume on stocks_extends.code = volume.code and stocks_extends.date = volume.date and stocks_extends.type='S'")
            ->join("left join k_data on stocks_extends.code = k_data.code and stocks_extends.date = k_data.date and stocks_extends.type='S'")
            ->join("left join stocks_info on stocks_extends.code = stocks_info.code and stocks_extends.type='S'")
            ->join('left join stocks_report on stocks_extends.code = stocks_report.code')
            ->join('left join stocks_growth on stocks_extends.code = stocks_growth.code')
            ->field('name, stocks_extends.code, stocks_extends.date, p_change, vol_break_5d, vol_break_10d, vol_break_20d, close, industry, pe, timetomarket, stocks_info.bvps, profits_yoy, mbrg')
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

        $lastData = M('stocks_extends')->field('date')->order('date desc')->limit(1)->find();
        $lastDay = $lastData['date'];
        $map['stocks_extends.date'] = array('eq', $lastDay);

        $map['stocks_extends.type'] = 'S';
        $map['p_change'] = array('elt', -2.00);

        if(!empty($range)) {
            switch($range) {
                case 1:
                    $map['p_change'] = array('elt', -8.00);
                    break;
                case 2:
                    $map['p_change'] = array(array('gt', -8.00), array('elt', -5.00));
                    break;
                case 3:
                    $map['p_change'] = array(array('gt', -5.00), array('elt', -2.00));
                    break;
                default:
                    break;
            }
        }

        $count = M('stocks_extends')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $order = !isset($sort) ? 'p_change' : ($desc == 1 ? "$sort desc" : "$sort");

        $list = M('stocks_extends')
            ->where($map)
            ->join("left join volume on stocks_extends.code = volume.code and stocks_extends.date = volume.date and stocks_extends.type='S'")
            ->join("left join k_data on stocks_extends.code = k_data.code and stocks_extends.date = k_data.date and stocks_extends.type='S'")
            ->join("left join stocks_info on stocks_extends.code = stocks_info.code and stocks_extends.type='S'")
            ->join('left join stocks_report on stocks_extends.code = stocks_report.code')
            ->join('left join stocks_growth on stocks_extends.code = stocks_growth.code')
            ->field('name, stocks_extends.code, stocks_extends.date, p_change, vol_break_5d, vol_break_10d, vol_break_20d, close, industry, pe, timetomarket, stocks_info.bvps, profits_yoy, mbrg')
            ->order($order)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Perday:down');
    }
}