"""
代码用途: 下载EndoMapper Simulator数据集的脚本
作者: Hsieh Cheng-Tai @IRMV
邮箱: hsiehtpe_sjtu@sjtu.edu.cn
创建日期: 2025年3月18日
最后修改日期: 2025年3月18日
版权所有: © 2025 Hsieh Cheng-Tai @IRMV, 保留所有权利

使用说明:
1. 在脚本中指定下载路径，开始下载

注意事项:
- 未经许可， 严禁转载authoken, 请勿泄露给IRMV实验室以外的人员
- 该脚本是为了下载EndoMapper Simulator数据集, 需要从Synapse网站下载并且未经处理
- 可以在脚本指定数据集的ID, 下载到指定路径
- 有关更多数据集下载信息(如完整数据集ID syn26707219), 可以查看Synapse网站查询EndoMapper数据集, 亦可以邮件联系该文档作者



Purpose: Script to download the EndoMapper Simulator dataset
Author: Hsieh Cheng-Tai @IRMV
email: hsiehtpe_sjtu@sjtu.edu.cn
Created Date: March 18, 2025
Last Modified Date: March 18, 2025
Copyright: © 2025 Hsieh Cheng-Tai @IRMV, All rights reserved

Usage Instructions:
1. Specify the download path in the script and start the download

Notes:
- It is strictly prohibited to reprint the authoken without permission; \
    do not disclose it to anyone outside the IRMV lab.
- This script is for downloading the EndoMapper Simulator dataset, which needs to be downloaded \
    from the Synapse website and should be unprocessed.
- You can specify the dataset ID in the script to download it to the specified path.
- For more information on dataset downloads (such as the complete dataset SynID), \
    you can check the Synapse website to query the EndoMapper dataset or contact the author of this document via email.

数据集使用条款 Terms of Use and License @Pablo Azagra (pazagra) :
Our **conditions **for accessing the data are:
1.  Limited to research on how to obtain relevant medical information from images or video
2.  Redistribution of the data is not allowed.
3.  Requires a **Statement of Intended Use**, which includes a description of how you intend to use this data.
4.   You further agree to **cite **the DOI of the collection and the publication in any publication resulting from this content as follows:
       *Azagra, P. et al. Endomapper dataset of complete calibrated endoscopy procedures. https://doi.org/10.7303/syn26707219331 (2022)
       *Azagra, P., Sostres, C., Ferrández, Á. et al. Endomapper dataset of complete calibrated endoscopy procedures. Sci Data 10, 671 (2023).  https://doi.org/10.1038/s41597-023-02564-7
5.   Images of the collection can be included in the scientific citing publications
6.   Video segments can be used to produce multimedia material in the citing scientific publications.
7.   The Universidad de Zaragoza will create a register of users of the dataset. The University of Zaragoza will store your Full Name, Synapse User ID, and Statement of Intended Use Any questions or concerns may be directed to The Unizar DPO at the following email address: dpd@unizar.es
    
"""

import synapseclient 
import synapseutils 
 
syn = synapseclient.Synapse() 
# This is the authentication token created by Hsieh Cheng-Tai, for the user who has access to the data
syn.login(authToken="eyJ0eXAiOiJKV1QiLCJraWQiOiJXN05OOldMSlQ6SjVSSzpMN1RMOlQ3TDc6M1ZYNjpKRU9VOjY0NFI6VTNJWDo1S1oyOjdaQ0s6RlBUSCIsImFsZyI6IlJTMjU2In0.eyJhY2Nlc3MiOnsic2NvcGUiOlsidmlldyIsImRvd25sb2FkIl0sIm9pZGNfY2xhaW1zIjp7fX0sInRva2VuX3R5cGUiOiJQRVJTT05BTF9BQ0NFU1NfVE9LRU4iLCJpc3MiOiJodHRwczovL3JlcG8tcHJvZC5wcm9kLnNhZ2ViYXNlLm9yZy9hdXRoL3YxIiwiYXVkIjoiMCIsIm5iZiI6MTc0MjE4MzM0NywiaWF0IjoxNzQyMTgzMzQ3LCJqdGkiOiIxNzY3NiIsInN1YiI6IjM1Mjc2MTgifQ.pZCDnCtYGnceBSui5VDWLFEhWBbYNQ71OlTG9f19SABBYjuzK-AmFLNwKd5pl0N2h3c-avRjklti7pZiS_KfKA-0aiJAdlJ1YJk9otcKzqFtQCO246DkhoLHDxCQz7aU46biazGrfZRWuJXkakwtKDi1B5A7NxKf95HATDfHSgsWCjH7weV_D9X7f77ZHRxcNdQqrcB2QrM30V7r03CyeQGRrQ8-es9uwBGEwbNMKwmaIVCi3IgaopsAVZcd0gasBtY7xnEOq_6WwRR9U1MyyZ8jBeyTIlQu1lSawOs_oa5z8sl199ImYWItO8prvWnj3ltOybkyhwQ9WD15kjLFag") 
# This is the ID of the slected dataset in Synapse you want to download
files = synapseutils.syncFromSynapse(syn,'syn30304069', path='~/Codes/Dataset/endomapper_simulator_dataset')