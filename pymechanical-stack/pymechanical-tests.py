from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

app = App()
app.update_globals(globals())
print(app)

g_path = "test_runs/beam_0/mode_shapes/beam_0_mode_1.vtk"
geometry_path = download_file("Valve.pmdb", "pymechanical", "embedding")
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import.Import(geometry_path)

app.plot()
delete_downloads()
app.new()