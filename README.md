## Project machine learing

# Hierarchical, multi-label prediction for automated cell type identification

### Klaas Goethals and Iwijn Voeten

### colaborative:
- port forward on port 8888
- `max_buffer_size` is set to give jupyter more memory, this causes less kernel crashes
```
jupyter-lab --ServerApp.max_buffer_size=8589934592 --collaborative --port=8888 --ip=0.0.0.0 --ServerApp.password='argon2:\$argon2id\$v=19\$m=10240,t=10,p=8\$vXBbTolcNr+BuyBggEBjCg\$ZLiqVTLZRn6Petn/vgNzzQ' --ServerApp.password_required=True -y
```
