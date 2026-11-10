
output "public_ip" {
  description = "Elastic IP of the server"
  value       = aws_instance.my_instance.public_ip
}
output "private_ip" {
  description = "Private IP inside the VPC"
  value       = aws_instance.my_instance.private_ip
}
output "ssh_command" {
  value = "ssh -i monitor_key ubuntu@${aws_instance.my_instance.public_ip}"
}

output "api_docs_url" {
  value = "http://${aws_instance.my_instance.public_ip}:8000/docs"
}

output "grafana_url" {
  value = "http://${aws_instance.my_instance.public_ip}:3000"
}
