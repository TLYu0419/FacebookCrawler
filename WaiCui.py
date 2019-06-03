import pandas as pd
import datetime ,time, pysftp, os, re
import shutil
from selenium import webdriver

ADPW = pd.read_excel(r'\\vibo\nfs\CHPublic\�Ȥ�A�ȨƷ~��\�ʦ��޲z��\Calvin\WaiCui.pptx',
                     sheet_name='ADPW',
                     dtype=str)
# �]�w�b���K�X
Account = ADPW.AD[0]
Password = ADPW.PW[0]
List = pd.read_excel(r'\\vibo\nfs\CHPublic\�Ȥ�A�ȨƷ~��\�ʦ��޲z��\Calvin\WaiCui.pptx',sheet_name='List',dtype='str')

path = 'C:/Users/' + Account + '/Downloads/'
today = datetime.datetime.now().strftime('%Y%m%d')

try:
    os.mkdir(path + '/WaiCui/')
except:
    time.sleep(0.1)
    
for i in range(len(List)):    
    
    # �]�w�򥻬d�߸��
    ActionId = str(List.�e�קO�N��[i])
    CompanyID = str(List.���q�N��[i])
    FTP_AD = str(List.FTP�b��[i])
    FTP_PW = str(List.FTP�K�X[i])
    
    print('Dealing with: ' + List.�e�קO[i] + '_' + List.���q[i])
    print('Start Time Log: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # �z�LSelenium�}��Chrome�s����
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(1200)
    driver.implicitly_wait(1800)
    driver.get('http://colweb.tstartel.com/colweb/adLoginLogin')
    time.sleep(2)
    
    # ��J�b���K�X
    driver.find_element_by_id('aduser').send_keys(Account)
    time.sleep(0.5)
    driver.find_element_by_id('password').send_keys(Password)
    time.sleep(0.5)
    driver.find_element_by_xpath('//button[@class="btn btn-default"]').click()
    time.sleep(0.5)
    
    # �i�}��Ƨ�
    time.sleep(2)
    driver.find_element_by_xpath('//i[@class="jstree-icon jstree-ocl"]').click()
    time.sleep(0.5)
    driver.find_elements_by_xpath('//i[@class="jstree-icon jstree-ocl"]')[1].click()
    time.sleep(0.5)
    driver.find_element_by_id('extRem1_anchor').click()
    time.sleep(10)

    # ��ܼ�����ƪ�����G�e�קO�B�e�פ��q�P�e�ת��A
    webdriver.support.ui.Select(driver.find_element_by_id('actionId')).select_by_value(ActionId)
    webdriver.support.ui.Select(driver.find_element_by_id('company')).select_by_value(CompanyID)
    webdriver.support.ui.Select(driver.find_element_by_id('type')).select_by_value("OPEN")
    # �e�X�d��
    driver.find_element_by_id('btnQry').click()
    time.sleep(1)
    # ���ﶵ�ب��I���U��
    driver.find_element_by_id('cb_grid').click()
    time.sleep(2)
    driver.find_element_by_id('btnDown').click()
    time.sleep(30)
    print('Download Succed!')
    
    # �h��ܮw�s��
    shutil.move(path + today + '.zip',
                '//vibo/nfs/CHPublic/�Ȥ�A�ȨƷ~��/�ʦ��޲z��/Calvin/WaiCui/' + today + '_' + ActionId + '_' + CompanyID + '.zip')    
    print('Move Succed!')
    
    # �N�ɮפW�Ǧ�FTP
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection(host = "172.23.1.44",
                             username = FTP_AD,
                             password = FTP_PW,
                             cnopts = cnopts)
    
    sftp.put(localpath = '//vibo/nfs/CHPublic/�Ȥ�A�ȨƷ~��/�ʦ��޲z��/Calvin/WaiCui/' + today + '_' + ActionId + '_' + CompanyID + '.zip',
             remotepath = '/ACCLIST/' + today + '_' + ActionId + '_' + CompanyID + '.zip')
    
    list = sftp.listdir('/ACCLIST/')
    for j in list:
        # �˴��ɮ׮榡�ŦXDummy�W�Ǫ����Y��
        if bool(re.search('[0-9]{8}_[0-9]{2}_[0-9]{6}.*.zip', j)) == True:
            # �˴�����O�_�W�L3��
            if (datetime.datetime.today().date()- datetime.datetime.strptime(j[:8], "%Y%m%d").date()).days > 3:
                print('Remove: ' + j)
                sftp.remove('/ACCLIST/' + j)
                
    sftp.close()
    print('Upload SFTP Succed!')
    print('End Time Log: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('-----------------\n\n')
    driver.quit()