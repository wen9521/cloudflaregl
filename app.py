from modules.cache_management import clear_cache_handler
from modules.waf_rules import add_waf_handler
from modules.domain_status import check_domain_status_handler
from modules.load_balancer import create_load_balancer_handler
from modules.performance_optimization import toggle_brotli_handler

# 添加所有命令处理程序
dispatcher.add_handler(clear_cache_handler)
dispatcher.add_handler(add_waf_handler)
dispatcher.add_handler(check_domain_status_handler)
dispatcher.add_handler(create_load_balancer_handler)
dispatcher.add_handler(toggle_brotli_handler)