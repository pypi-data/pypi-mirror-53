# dfs_tool

It is a HDFS cli tool. You can use it to manage your HDFS file system.

It calls the [WebHDFS](https://hadoop.apache.org/docs/r1.0.4/webhdfs.html) API.

# Configuration
You need to put a config file. By default, the config file is at `~/.dfs_tool/config.json`, however you can change it's location by setting environment variable `DFS_TOOL_CFG`

The configuration looks like below:
```json
{
    "api_base_uri": "https://my_hdfs_cluster.com/gateway/ui/webhdfs/v1/",
    "username": "superman",
    "password": "mypassword",
    "io_chunk_size": 16777216
}
```

In some case, server uses certificate to authenticate client, then you can config like below:
```json
{
    "api_base_uri": "https://my_hdfs_cluster.com/gateway/ui/webhdfs/v1/",
    "auth_cert": "/Users/shizhong/.dfs_tool/sso_client.cer",
    "auth_key" : "/Users/shizhong/.dfs_tool/sso_client.key",
    "ca_cert"  : "/Users/shizhong/.dfs_tool/CombinedDigicertCA.cer"
}
```

* `api_base_url`: You need to put your WebHDFS endpoint here
* `username`: You need to specify your HDFS account username
* `password`: You need to specify your HDFS account password
* `io_chunk_size`: optional, if not set, the default value is 1048576. It is the chunk size for downloading data from HDFS or uploading data to HDFS, you may want to bump this value if your bandwidth is high

# Command supported
```
dfs_tool ls [-R]          <remote_path>                            -- list directory or file
dfs_tool download [-R]    <remote_filename> <local_path>           -- download file
dfs_tool cat              <remote_filename>                        -- cat a file
dfs_tool mkdir            <remote_dir_name>                        -- make a directory
dfs_tool rm [-RM]         <remote_path>                            -- remove a file or directory
dfs_tool upload [-R] [-F] <local_filename> <remote_path>           -- upload file
dfs_tool mv               <source_location> <destination_location> -- move file or directory
```

# Options
Some command support options, here are options:
* `-R`
It means "recursive"

* `-F`
It means "force", in upload command, when `-F` is specified, it will override the file already exist there.

* `-M`
In "rm" command, you can specify a pattern to match the files you want to delete, for example:
```
dfs_tool rm -M "/tmp/*.parquet"
```