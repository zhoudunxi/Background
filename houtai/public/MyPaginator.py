from django.core.paginator import Paginator, EmptyPage

class MyPaginator(object):
    """
    When try 'EmptyPage' error, return the last page, 
    else return the firt page with 10 records. 
    """
    def __init__(self, data, nums_perpage, page_num):
        #The objects for pagination.
        self.data = data
        #The numbers of per page.
        self.nums_perpage = nums_perpage
        if not self.nums_perpage or not isinstance(self.nums_perpage, 
            int) or self.nums_perpage <= 0:
            self.nums_perpage = 10
        #The page number.
        self.page_num = page_num
        if not self.page_num or not isinstance(self.page_num, 
            int) or self.page_num <= 0:
            self.page_num = 1
    

    def mypaginator(self):
        """
        :return: 
            object_list, list, objects in page.
            count, int, all the records number.
            pagecount, int, all the pages number.
            pagelist, list, a list of page numbers.
            has_previous, bool, whether has previous page.
            has_next, bool, whether has next page.
        """
        data = Paginator(self.data, self.nums_perpage)
        try:
            page = data.page(self.page_num)
        except EmptyPage:
            page = data.page(data.num_pages)
        return {'object_list':page.object_list,
            'attribute':{
                'count':data.count,
                'pagecount':data.num_pages,
                'pagelist':data.page_range,
                'has_previous':page.has_previous(),
                'has_next':page.has_next()
            }
        }