# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from trytond.pool import PoolMeta
from trytond.modules.project_product import get_service_goods_aux


class Work:
    __name__ = 'project.work'
    __metaclass__ = PoolMeta

    @classmethod
    def _get_revenue(cls, works):
        """Return the quantity * list_price for goods works"""
        return get_service_goods_aux(
            works,
            super(Work, cls)._get_revenue,
            lambda work: (Decimal(str(work.quantity))
                * (work.list_price or Decimal(0))))

    @classmethod
    def _get_cost(cls, works):
        """Return the quantity * product's cost price for goods works"""

        works_c = works
        costs = {}
        if hasattr(cls, 'purchase_lines'):
            work_p = [x for x in works if x.purchase_lines]
            costs = super(Work, cls)._get_cost(work_p)
            works_c = [x for x in works if not x.purchase_lines]

        costs.update(get_service_goods_aux(
            works_c,
            super(Work, cls)._get_cost,
            lambda work: (Decimal(str(work.quantity)) *
                work.product_goods.cost_price)))
        return costs
