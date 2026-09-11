# System State Freezing Single Exceptional Fix

This example demonstrates the concept of 'Freezing State in Error' and 'Single Exceptional Change Management'. It simulates a system that, upon encountering a critical error during a regular operation, freezes its state to prevent further uncontrolled modifications. While frozen, all regular operations are blocked. The system then allows only a single, controlled, exceptional fix to rectify the specific issue, after which it unfreezes and resumes normal operations.

## Language

`python`

## How to Run

Save the code as `main.py`.
Run from your terminal: `python main.py`

## Original Article

This example accompanies the Turkish article: [Hata Durumunda Durum Dondurma: Tek İstisnai Değişiklik Yönetimi](https://fatihsoysal.com/blog/hata-durumunda-durum-dondurma-tek-istisnai-degisiklik-yonetimi/).

## License

MIT — see [LICENSE](LICENSE).
