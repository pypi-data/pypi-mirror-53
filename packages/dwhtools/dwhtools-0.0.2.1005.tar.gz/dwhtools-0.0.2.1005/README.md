# Entwicklung und testen
Test erfolgt über den Upload nach Pypi  
In Databricks kann dann mit folgendem Code getestet werden:  
<br>
import pkg_resources  
dbutils.library.installPyPI("dwhtools")  
dbutils.library.restartPython()  
pkg_resources.get_distribution("dwhtools").version