/**
 * Copyright (c) 2014 - 2019, Nordic Semiconductor ASA
 *
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this
 *    list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form, except as embedded into a Nordic
 *    Semiconductor ASA integrated circuit in a product or a software update for
 *    such product, must reproduce the above copyright notice, this list of
 *    conditions and the following disclaimer in the documentation and/or other
 *    materials provided with the distribution.
 *
 * 3. Neither the name of Nordic Semiconductor ASA nor the names of its
 *    contributors may be used to endorse or promote products derived from this
 *    software without specific prior written permission.
 *
 * 4. This software, with or without modification, must only be used with a
 *    Nordic Semiconductor ASA integrated circuit.
 *
 * 5. Any software provided in binary form under this license must not be reverse
 *    engineered, decompiled, modified and/or disassembled.
 *
 * THIS SOFTWARE IS PROVIDED BY NORDIC SEMICONDUCTOR ASA "AS IS" AND ANY EXPRESS
 * OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY, NONINFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL NORDIC SEMICONDUCTOR ASA OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
 * GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
 * OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 */
/**
 * scans for ble advertisements
 * based on the ble_central/ble_app_hrs_c example
 */
#include <stdint.h>
#include <stdio.h>
#include "nrf_sdh.h"
#include "nrf_sdh_ble.h"
#include "nrf_log.h"
#include "nrf_log_ctrl.h"
#include "nrf_log_default_backends.h"
#include "nrf_ble_scan.h"
#include "ble_advdata.h"
//#include "ble_bas.h"
#include "Battery Level/battery_voltage.h"

#define APP_BLE_CONN_CFG_TAG        1                                   /**< A tag identifying the SoftDevice BLE configuration. */
#define SCAN_DURATION_WITELIST      3000                                /**< Duration of the scanning in units of 10 milliseconds. */
#define DEV_NAME_LEN                ((BLE_GAP_ADV_SET_DATA_SIZE_MAX + 1) - \
                                    AD_DATA_OFFSET)                     /**< Determines the device name length. */

NRF_BLE_SCAN_DEF(m_scan);                                           /**< Scanning module instance. */

#define MAX_ADDRESS_COUNT 100

uint8_t address_list[MAX_ADDRESS_COUNT][BLE_GAP_ADDR_LEN] = {0};
int address_list_length = 0;

/**< Scan parameters requested for scanning and connection. */
static ble_gap_scan_params_t const m_scan_param =
{
    .active        = 0x01,
    .interval      = NRF_BLE_SCAN_SCAN_INTERVAL,
    .window        = NRF_BLE_SCAN_SCAN_WINDOW,
    .filter_policy = BLE_GAP_SCAN_FP_ACCEPT_ALL, //BLE_GAP_SCAN_FP_WHITELIST,
    .timeout       = SCAN_DURATION_WITELIST,
    .scan_phys     = BLE_GAP_PHY_1MBPS,
};

/**@brief Function for initializing the BLE stack.
 *
 * @details Initializes the SoftDevice and the BLE event interrupt.
 */
static void ble_stack_init(void)
{
    ret_code_t err_code;

    err_code = nrf_sdh_enable_request();
    APP_ERROR_CHECK(err_code);

    // Configure the BLE stack using the default settings.
    // Fetch the start address of the application RAM.
    uint32_t ram_start = 0;
    err_code = nrf_sdh_ble_default_cfg_set(APP_BLE_CONN_CFG_TAG, &ram_start);
    APP_ERROR_CHECK(err_code);

    // Enable BLE stack.
    err_code = nrf_sdh_ble_enable(&ram_start);
    APP_ERROR_CHECK(err_code);
}

/**@brief Function to start scanning.
 */
static void scan_start(void)
{
    NRF_LOG_INFO("Starting scan.");
    APP_ERROR_CHECK(nrf_ble_scan_start(&m_scan));
}

bool address_list_contains(const uint8_t address[]) {
    for (int i = 0; i < address_list_length; i++) {
        if (address_list[i][0] == address[0]
            && address_list[i][1] == address[1]
            && address_list[i][2] == address[2]
            && address_list[i][3] == address[3]
            && address_list[i][4] == address[4]
            && address_list[i][5] == address[5]) {
            
            return true;
        }
    }
    
    return false;
}

bool address_list_add(const uint8_t address[]) {
    if (address_list_length < MAX_ADDRESS_COUNT) {
        memcpy(address_list[address_list_length], address, BLE_GAP_ADDR_LEN);
        address_list_length++;
    }
}

void print_address(const ble_gap_evt_adv_report_t* p_adv_report) {
    NRF_LOG_INFO("addr: %02x:%02x:%02x:%02x:%02x:%02x",
       p_adv_report->peer_addr.addr[5],
       p_adv_report->peer_addr.addr[4],
       p_adv_report->peer_addr.addr[3],
       p_adv_report->peer_addr.addr[2],
       p_adv_report->peer_addr.addr[1],
       p_adv_report->peer_addr.addr[0]);
}

void print_name(const ble_gap_evt_adv_report_t* p_adv_report) {
    uint16_t offset = 0;
    char name[DEV_NAME_LEN] = { 0 };
    
    uint16_t length = ble_advdata_search(p_adv_report->data.p_data, p_adv_report->data.len, &offset, BLE_GAP_AD_TYPE_COMPLETE_LOCAL_NAME);
    if (length == 0) {
        // Look for the short local name if it was not found as complete.
        length = ble_advdata_search(p_adv_report->data.p_data, p_adv_report->data.len, &offset, BLE_GAP_AD_TYPE_SHORT_LOCAL_NAME);
    }
    
    if (length != 0) {
        memcpy(name, &p_adv_report->data.p_data[offset], length);
        NRF_LOG_INFO("name: %s", nrf_log_push(name));
    }
}

void print_manufacturer_data(const ble_gap_evt_adv_report_t* p_adv_report) {
    uint16_t offset = 0;
    uint16_t length = ble_advdata_search(p_adv_report->data.p_data, p_adv_report->data.len, &offset, BLE_GAP_AD_TYPE_MANUFACTURER_SPECIFIC_DATA);
    
    if (length != 0) {
        char data_string[1024] = { 0 };
        char* pos = data_string;
        for (int i = 0; i < length && i < 512; i++) {
            sprintf(pos, "%02x", p_adv_report->data.p_data[offset+i]);
            pos += 2;
        }
        
        NRF_LOG_INFO("manufacturer data: %s", nrf_log_push(data_string));
    }
}

static void scan_evt_handler(scan_evt_t const * p_scan_evt)
{
//  ้ถ้า scan แล้วไม่เจอในเวลาที่กำหนด ให้ timeout แล้ว scan ใหม่
    if (p_scan_evt->scan_evt_id == NRF_BLE_SCAN_EVT_SCAN_TIMEOUT) {
        NRF_LOG_INFO("Scan timed out.");
        scan_start();
        return;
    }

    if (address_list_contains(p_scan_evt->params.filter_match.p_adv_report->peer_addr.addr) != false)
        return;

    address_list_add(p_scan_evt->params.filter_match.p_adv_report->peer_addr.addr);

    /*switch (p_scan_evt->params.filter_match.p_adv_report->peer_addr.addr_type) {
        case BLE_GAP_ADDR_TYPE_PUBLIC:
            NRF_LOG_INFO("address type BLE_GAP_ADDR_TYPE_PUBLIC");
            break;
        case BLE_GAP_ADDR_TYPE_RANDOM_STATIC:
            NRF_LOG_INFO("address type BLE_GAP_ADDR_TYPE_RANDOM_STATIC");
            break;
        case BLE_GAP_ADDR_TYPE_RANDOM_PRIVATE_RESOLVABLE:
            NRF_LOG_INFO("address type BLE_GAP_ADDR_TYPE_RANDOM_PRIVATE_RESOLVABLE");
            break;
        case BLE_GAP_ADDR_TYPE_RANDOM_PRIVATE_NON_RESOLVABLE:
            NRF_LOG_INFO("address type BLE_GAP_ADDR_TYPE_RANDOM_PRIVATE_NON_RESOLVABLE");
            break;
        case BLE_GAP_ADDR_TYPE_ANONYMOUS:
            NRF_LOG_INFO("address type BLE_GAP_ADDR_TYPE_ANONYMOUS");
            break;
    }*/
    
    print_address(p_scan_evt->params.filter_match.p_adv_report);
    print_name(p_scan_evt->params.filter_match.p_adv_report);
    NRF_LOG_INFO("rssi: %d", p_scan_evt->params.filter_match.p_adv_report->rssi);
    print_manufacturer_data(p_scan_evt->params.filter_match.p_adv_report);
}

/**@brief Function for initialization scanning and setting filters.
 */
static void scan_init(void)
{
    ret_code_t          err_code;
    nrf_ble_scan_init_t init_scan;
    memset(&init_scan, 0, sizeof(init_scan));

    init_scan.p_scan_param     = &m_scan_param;
    init_scan.connect_if_match = false;
    init_scan.conn_cfg_tag     = APP_BLE_CONN_CFG_TAG;

    err_code = nrf_ble_scan_init(&m_scan, &init_scan, scan_evt_handler);
    APP_ERROR_CHECK(err_code);
}


int main(void)
{
    ret_code_t err_code;

    err_code = NRF_LOG_INIT(NULL);
    APP_ERROR_CHECK(err_code);
    NRF_LOG_DEFAULT_BACKENDS_INIT();

    ble_stack_init();
    scan_init();
    battery_voltage_init();
    // Start execution.
    NRF_LOG_INFO("Start scan");
    scan_start();

    // Enter main loop.
    for (;;)
    {
        NRF_LOG_FLUSH();

        __WFI(); 
        __SEV();
        __WFE();
    }
}