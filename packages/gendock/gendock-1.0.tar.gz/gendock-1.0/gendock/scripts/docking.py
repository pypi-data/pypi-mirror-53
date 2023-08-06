import os
import csv
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
import openbabel as ob
import subprocess
import sys

def osCommand(command):
    c  = subprocess.Popen(command, shell=True)
    try:
        c.wait(120)
    except subprocess.TimeoutExpired:
        print("Command timed out")
        c.kill()
        pass
    except Exception:
        pass

def get_energy(file_name):
    file = open(file_name) 
    lines = file.readlines() 
    file.close() 
    line = lines[1] 
    result = float(line.split(':')[1].split()[0])  #splits between : and 0, the binding energy is always between these on line[1]
    return result

def process(mol, receptors, l_num, name):
    print("Trying to acquire ligand attributes and binding energy...")
    temp_array = []
    recept_num = 1
    temp_array.append('ligand_'+str(l_num))
    temp_array.append(Descriptors.MolWt(mol))
    temp_array.append(Descriptors.MolLogP(mol))
    temp_array.append(Chem.MolToSmiles(mol))
    if mol.HasProp('NSC'):
        temp_array.append(mol.GetProp('NSC'))
    elif mol.HasProp('E_NSC'):
        temp_array.append(mol.GetProp('E_NSC'))
    else:
        temp_array.append('N/A')
    for receptor in receptors:
        ligand_file = os.path.join('data', str(name), 'vina_files', 'ligand_'+str(l_num)+'-'+receptor+'.pdbqt')
        temp_array.append(str(get_energy(ligand_file)))
    csv_fname = str(name)+"_results.csv"
    csv_file = os.path.join('data', name, csv_fname)
    with open(csv_file, "a") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(temp_array)
    print("Ligand attributes and binding energy acquired and appended to csv file")

def makedir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)

def convertMol(pdb, pdbqt):
    obCon = ob.OBConversion()
    obCon.SetInAndOutFormats('pdb', 'pdbqt')
    mol = ob.OBMol()
    obCon.ReadFile(mol, pdb)
    obCon.WriteFile(mol, pdbqt)
    os.remove(pdb)

def docking(pdbqt_file, receptors, vina_files_dir, molnum):
    recept_num = 0
    for receptor in receptors:
        # run vina
        print("Docking ligand " + str(molnum) + " with " + receptor)
        f_out_pdbqt = os.path.join(vina_files_dir, 'ligand_' + str(molnum) + '-' + str(receptor) + '.pdbqt')
        f_out_log = os.path.join(vina_files_dir, 'ligand_' + str(molnum) + '-' + str(receptor) + '.txt')
        # python = sys.executable.split(os.sep)
        # vina = os.path.join(os.sep, *python[:-1], 'vina')
        rpath = os.path.join('receptors', receptor)
        vina_command = 'vina --config ' + rpath + '-config.txt --ligand ' + pdbqt_file + ' --out ' + f_out_pdbqt + ' --log ' + f_out_log
        print(vina_command)
        osCommand(vina_command)
        recept_num += 1

def moldocking(name, start_ligand, receptors):
    data_dir = os.path.join('data', name)
    vina_ligands_dir = os.path.join(data_dir, 'vina_ligands')
    makedir(vina_ligands_dir)
    vina_files_dir = os.path.join(data_dir, 'vina_files')
    makedir(vina_files_dir)
    #start docking:
    suppl = Chem.SDMolSupplier(os.path.join(data_dir, str(name)+'.sdf'))
    pdb_file = os.path.join(data_dir, 'ligand.pdb')
    pdbqt_file = pdb_file + "qt"
    molnum = 1
    for mol in suppl:
        if molnum >= start_ligand:
            AllChem.EmbedMolecule(mol)
            AllChem.UFFOptimizeMolecule(mol)
            AllChem.MolToPDBFile(mol, pdb_file)
            convertMol(pdb_file, pdbqt_file)
            docking(pdbqt_file, receptors, vina_files_dir, molnum)
            os.remove(pdbqt_file)
            process(mol, receptors, molnum, name)
        else:
            pass
        molnum += 1
