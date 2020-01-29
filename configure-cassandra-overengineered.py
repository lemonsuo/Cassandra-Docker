#!/usr/bin/python

# "cluster_name num_tokens allocate_tokens_for_keyspace allocate_tokens_for_local_replication_factor initial_token hinted_handoff_enabled hinted_handoff_disabled_datacenters max_hint_window_in_ms hinted_handoff_throttle_in_kb max_hints_delivery_threads hints_directory hints_flush_period_in_ms max_hints_file_size_in_mb hints_compression batchlog_replay_throttle_in_kb authenticator authorizer role_manager network_authorizer roles_validity_in_ms roles_update_interval_in_ms permissions_validity_in_ms permissions_update_interval_in_ms credentials_validity_in_ms credentials_update_interval_in_ms partitioner data_file_directories commitlog_directory cdc_enabled cdc_raw_directory disk_failure_policy commit_failure_policy prepared_statements_cache_size_mb key_cache_size_in_mb key_cache_save_period key_cache_keys_to_save row_cache_class_name row_cache_size_in_mb row_cache_save_period row_cache_keys_to_save counter_cache_size_in_mb counter_cache_save_period counter_cache_keys_to_save saved_caches_directory commitlog_sync_batch_window_in_ms commitlog_sync_group_window_in_ms commitlog_sync commitlog_sync_period_in_ms periodic_commitlog_sync_lag_block_in_ms commitlog_segment_size_in_mb commitlog_compression seed_provider seeds concurrent_reads concurrent_writes concurrent_counter_writes concurrent_materialized_view_writes file_cache_size_in_mb buffer_pool_use_heap_if_exhausted disk_optimization_strategy memtable_heap_space_in_mb memtable_offheap_space_in_mb memtable_cleanup_threshold memtable_allocation_type repair_session_space_in_mb commitlog_total_space_in_mb memtable_flush_writers cdc_total_space_in_mb cdc_free_space_check_interval_ms index_summary_capacity_in_mb index_summary_resize_interval_in_minutes trickle_fsync trickle_fsync_interval_in_kb storage_port ssl_storage_port listen_address listen_interface listen_interface_prefer_ipv6 broadcast_address listen_on_broadcast_address internode_authenticator start_native_transport native_transport_port native_transport_port_ssl native_transport_max_threads native_transport_max_frame_size_in_mb native_transport_frame_block_size_in_kb native_transport_max_concurrent_connections native_transport_max_concurrent_connections_per_ip native_transport_allow_older_protocols native_transport_idle_timeout_in_ms rpc_address rpc_interface rpc_interface_prefer_ipv6 broadcast_rpc_address rpc_keepalive internode_send_buff_size_in_bytes internode_recv_buff_size_in_bytes incremental_backups snapshot_before_compaction auto_snapshot column_index_size_in_kb column_index_cache_size_in_kb concurrent_compactors concurrent_validations concurrent_materialized_view_builders compaction_throughput_mb_per_sec sstable_preemptive_open_interval_in_mb stream_entire_sstables stream_throughput_outbound_megabits_per_sec inter_dc_stream_throughput_outbound_megabits_per_sec read_request_timeout_in_ms range_request_timeout_in_ms write_request_timeout_in_ms counter_write_request_timeout_in_ms cas_contention_timeout_in_ms truncate_request_timeout_in_ms request_timeout_in_ms internode_application_send_queue_capacity_in_bytes internode_application_send_queue_reserve_endpoint_capacity_in_bytes internode_application_send_queue_reserve_global_capacity_in_bytes internode_application_receive_queue_capacity_in_bytes internode_application_receive_queue_reserve_endpoint_capacity_in_bytes internode_application_receive_queue_reserve_global_capacity_in_bytes slow_query_log_timeout_in_ms cross_node_timeout streaming_keep_alive_period_in_secs streaming_connections_per_host phi_convict_threshold endpoint_snitch dynamic_snitch_update_interval_in_ms dynamic_snitch_reset_interval_in_ms dynamic_snitch_badness_threshold server_encryption_options client_encryption_options internode_compression inter_dc_tcp_nodelay tracetype_query_ttl tracetype_repair_ttl enable_user_defined_functions enable_scripted_user_defined_functions windows_timer_interval transparent_data_encryption_options tombstone_warn_threshold tombstone_failure_threshold batch_size_warn_threshold_in_kb batch_size_fail_threshold_in_kb unlogged_batch_across_partitions_warn_threshold compaction_large_partition_warning_threshold_mb gc_log_threshold_in_ms gc_warn_threshold_in_ms max_value_size_in_mb back_pressure_enabled back_pressure_strategy otc_coalescing_strategy otc_coalescing_window_us otc_coalescing_enough_coalesced_messages otc_backlog_expiration_interval_ms ideal_consistency_level automatic_sstable_upgrade max_concurrent_automatic_sstable_upgrades audit_logging_options full_query_logging_options corrupted_tombstone_strategy diagnostic_events_enabled native_transport_flush_in_batches_legacy repaired_data_tracking_for_range_reads_enabled repaired_data_tracking_for_partition_reads_enabled report_unconfirmed_repaired_data_mismatches enable_materialized_views enable_sasi_indexes enable_transient_replication"

import yaml
import os

def getKey(confDoc, keys):
    for key in keys:
        # TODO: Make it possible to add new items to a list instead of replcaing already existing items
        if isinstance(confDoc, list):
            if (len(confDoc)-1) < key
                print("ERROR You cannot add an item to an array (TO BE IMPLEMENTED)")
                os._exit(1)
        confDoc = confDoc[key]

    return confDoc


def set_conf_doc(confDoc, keys, value):
    # TODO: Validate top level keys to giver user feedback in case of typos or the likes, so they know that "saved_caches_dictory" is spelled wrong and not a possible configuration
    confDoc = getKey(confDoc, keys[:-1])
    confDoc[keys[-1]] = value


yamlArraySplitter = "-"
yamlDictionarySplitter = ":"

with open('/opt/cassandra/conf/cassandra.yaml') as file:
    configurationDocument = yaml.safe_load(file)

    for envKey, envValue in os.environ.iteritems():
        if envKey.startswith("CASSANDRA_"):
            configToChange = (envKey.split("CASSANDRA_", 1)[1]).lower()

            nestedConfigurationToChange = ""

            nestedKeys = []

            index = 0

            print("LENGTH IS " + str(len(configToChange)))

            while index < len(configToChange):
                character = configToChange[index]

                index += 1

                if character != yamlArraySplitter and character != yamlDictionarySplitter:
                    nestedConfigurationToChange += character
                    continue
                else:
                    if character == yamlDictionarySplitter:
                        continue

                    nestedKeys.append(nestedConfigurationToChange)
                    nestedConfigurationToChange = ""

                # Plus one because that is the index which the user wants to insert a configuration variable

                if character == yamlArraySplitter:
                    nestedKeys.append(int(configToChange[index]))
                    index = index + 1

            # Man kan teste for om det er null og hvis det er kan man append eller adde i stedet for
            if len(nestedConfigurationToChange) != 0:
                nestedKeys.append(nestedConfigurationToChange)

            print '[%s]' % ', '.join(map(str, nestedKeys))

            set_conf_doc(configurationDocument, nestedKeys, envValue)
            # configurationDocument["seed_provider"][0]["parameters"][0]["seeds"] = envValue

    with open('/opt/cassandra/conf/cassandra.yaml', 'w') as file:
        yaml.safe_dump(configurationDocument, file)
