
variable "instance_type" {
  default = "m7i-flex.large"
  type    = string

}
variable "storage_size" {
  default = 25
  type    = number
}
variable "ami_id" {
  default = "ami-020ba0ae8c230ae28"
  type    = string
}
variable "env" {
  default = "prd"
  type    = string
}
variable "project_name" {
  type    = string
  default = "uptime-monitor"
}
variable "my_ip_cidr" {
  type        = string
  description = "Your public IPv4 in CIDR form, e.g. 203.0.113.5/32"
}
