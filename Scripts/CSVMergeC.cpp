#include <QApplication>
#include <QFileDialog>
#include <QTextStream>
#include <QMap>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    // Use the QFileDialog class to open a file selection dialog
    QString file1 = QFileDialog::getOpenFileName();
    QString file2 = QFileDialog::getOpenFileName();

    // Set the name of the column with the relational information
    QString columnName = QInputDialog::getText(nullptr, "Column Name", "Enter column name:");

    // Create a QMap to store the merged rows
    QMap<QString, QMap<QString, QString>> mergedRows;

    // Open the first input file and read the rows
    QFile file(file1);
    if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        QTextStream stream(&file);
        while (!stream.atEnd()) {
            QStringList fields = stream.readLine().split(",");
            QMap<QString, QString> row;
            for (int i = 0; i < fields.size(); ++i) {
                row[QString::number(i)] = fields[i];
            }
            mergedRows[row[columnName]] = row;
        }
        file.close();
    }

    // Open the second input file and read the rows
    file.setFileName(file2);
    if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        QTextStream stream(&file);
        while (!stream.atEnd()) {
            QStringList fields = stream.readLine().split(",");
            QMap<QString, QString> row;
            for (int i = 0; i < fields.size(); ++i) {
                row[QString::number(i)] = fields[i];
            }
            mergedRows[row[columnName]] = {...mergedRows[row[columnName]], ...row};
        }
        file.close();
    }

    // Use the QFileDialog class to open a save file dialog
    QString outputFile = QFileDialog::getSaveFileName();

    // Write the merged rows to the output file
    file.setFileName(outputFile);
    if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        QTextStream stream(&file);
        for (auto it = mergedRows.begin(); it != mergedRows.end(); ++it) {
            stream << it.value().values().join(",") << endl;
        }
        file.close();
   
